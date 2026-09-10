#include "shell.h"
#include "console.h"
#include "keyboard.h"
#include "string.h"
#include "timer.h"
#include "pmm.h"
#include "heap.h"
#include "io.h"
#include "../include/darknode.h"
#include "../drivers/rtc.h"

#define CMD_BUF 256

static char cmd_buf[CMD_BUF];
static int cmd_len = 0;

static void prompt(void) {
    console_write_color("darknode", DN_COLOR_ACCENT);
    console_write_color("@", DN_COLOR_DIM);
    console_write_color("kernel", DN_COLOR_OK);
    console_write_color(" $ ", DN_COLOR_DIM);
}

static void cmd_help(void) {
    console_write_color("Commands:\n", DN_COLOR_HEADER);
    console_write_color("  help      ", DN_COLOR_ACCENT); console_write("show this help\n");
    console_write_color("  clear     ", DN_COLOR_ACCENT); console_write("clear the screen\n");
    console_write_color("  version   ", DN_COLOR_ACCENT); console_write("show OS version\n");
    console_write_color("  time      ", DN_COLOR_ACCENT); console_write("show current time (RTC)\n");
    console_write_color("  uptime    ", DN_COLOR_ACCENT); console_write("show system uptime\n");
    console_write_color("  mem       ", DN_COLOR_ACCENT); console_write("show memory usage\n");
    console_write_color("  cpuinfo   ", DN_COLOR_ACCENT); console_write("show CPU information\n");
    console_write_color("  echo      ", DN_COLOR_ACCENT); console_write("echo text back\n");
    console_write_color("  reboot    ", DN_COLOR_ACCENT); console_write("reboot the system\n");
    console_write_color("  shutdown  ", DN_COLOR_ACCENT); console_write("halt the system\n");
}

static void cmd_version(void) {
    console_write_color(DARKNODE_NAME, DN_COLOR_ACCENT);
    console_write(" version ");
    console_write_color(DARKNODE_VERSION, DN_COLOR_OK);
    console_write(" (");
    console_write(DARKNODE_YEAR);
    console_write(") by ");
    console_write(DARKNODE_AUTHOR);
    console_write("\n");
}

static void cmd_mem(void) {
    console_write("Total:   ");
    console_write_dec(pmm_total_memory());
    console_write(" KiB\n");
    console_write("Pages:   ");
    console_write_dec(pmm_used_pages());
    console_write(" used / ");
    console_write_dec(pmm_free_pages());
    console_write(" free (");
    console_write_dec(PAGE_SIZE / 1024);
    console_write(" KiB each)\n");
    console_write("Heap:    ");
    console_write_dec((uint32_t)heap_used());
    console_write(" bytes used\n");
}

static void cmd_cpuinfo(void) {
    char vendor[13] = {0};
    uint32_t a, b, c, d;
    __asm__ volatile("cpuid" : "=a"(a),"=b"(b),"=c"(c),"=d"(d) : "a"(0));
    *(uint32_t *)&vendor[0] = b;
    *(uint32_t *)&vendor[4] = d;
    *(uint32_t *)&vendor[8] = c;
    console_write("Vendor: ");
    console_write_color(vendor, DN_COLOR_ACCENT);
    console_write("\n");
}

static void cmd_uptime(void) {
    uint32_t secs = timer_get_ticks() / 1000;
    uint32_t mins = secs / 60;
    secs %= 60;
    console_write("Uptime: ");
    console_write_dec(mins);
    console_write("m ");
    console_write_dec(secs);
    console_write("s\n");
}

static void cmd_time(void) {
    uint8_t h = rtc_read(0x04);
    uint8_t m = rtc_read(0x02);
    uint8_t s = rtc_read(0x00);
    /* BCD to binary */
    h = (h >> 4) * 10 + (h & 0x0F);
    m = (m >> 4) * 10 + (m & 0x0F);
    s = (s >> 4) * 10 + (s & 0x0F);
    char buf[9];
    buf[0] = '0' + h / 10; buf[1] = '0' + h % 10; buf[2] = ':';
    buf[3] = '0' + m / 10; buf[4] = '0' + m % 10; buf[5] = ':';
    buf[6] = '0' + s / 10; buf[7] = '0' + s % 10; buf[8] = '\0';
    console_write("Time: ");
    console_write_color(buf, DN_COLOR_ACCENT);
    console_write(" (UTC)\n");
}

NORETURN static void cmd_reboot(void) {
    console_write_color("Rebooting...\n", DN_COLOR_WARN);
    uint8_t good = 0x02;
    while (good & 0x02) good = inb(0x64);
    outb(0x64, 0xFE);
    __asm__ volatile("cli; hlt");
    __builtin_unreachable();
}

NORETURN static void cmd_shutdown(void) {
    console_write_color("Halting system.\n", DN_COLOR_WARN);
    /* ACPI shutdown via QEMU debug port */
    outw(0x604, 0x2000);
    __asm__ volatile("cli; hlt");
    __builtin_unreachable();
}

static void cmd_echo(const char *args) {
    console_write(args);
    console_write("\n");
}

static void execute(const char *cmd) {
    if (!*cmd) return;
    if (strcmp(cmd, "help") == 0)        cmd_help();
    else if (strcmp(cmd, "clear") == 0)  console_clear();
    else if (strcmp(cmd, "version") == 0) cmd_version();
    else if (strcmp(cmd, "time") == 0)   cmd_time();
    else if (strcmp(cmd, "uptime") == 0) cmd_uptime();
    else if (strcmp(cmd, "mem") == 0)    cmd_mem();
    else if (strcmp(cmd, "cpuinfo") == 0) cmd_cpuinfo();
    else if (strcmp(cmd, "reboot") == 0) cmd_reboot();
    else if (strcmp(cmd, "shutdown") == 0) cmd_shutdown();
    else if (strncmp(cmd, "echo ", 5) == 0) cmd_echo(cmd + 5);
    else if (strcmp(cmd, "echo") == 0) console_write("\n");
    else {
        console_write_color("unknown command: ", DN_COLOR_ERR);
        console_write(cmd);
        console_write_color("  (type 'help')\n", DN_COLOR_DIM);
    }
}

void shell_init(void) {
    cmd_len = 0;
    memset(cmd_buf, 0, CMD_BUF);
}

void shell_run(void) {
    prompt();
    while (1) {
        char c = keyboard_getchar();
        if (c == '\n') {
            console_putchar('\n');
            cmd_buf[cmd_len] = '\0';
            execute(cmd_buf);
            cmd_len = 0;
            memset(cmd_buf, 0, CMD_BUF);
            prompt();
        } else if (c == '\b') {
            if (cmd_len > 0) {
                cmd_len--;
                console_backspace();
            }
        } else if (cmd_len < CMD_BUF - 1) {
            cmd_buf[cmd_len++] = c;
            console_putchar(c);
        }
    }
}
