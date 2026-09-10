#include "../include/types.h"
#include "../include/darknode.h"
#include "../include/multiboot2.h"
#include "console.h"
#include "string.h"
#include "gdt.h"
#include "idt.h"
#include "timer.h"
#include "keyboard.h"
#include "pmm.h"
#include "heap.h"
#include "serial.h"
#include "shell.h"
#include "../drivers/rtc.h"
#include "../drivers/pci.h"

static void boot_banner(void) {
    console_set_color(DN_COLOR_ACCENT, DN_COLOR_BG);
    console_write("\n");
    console_write("  ____             _                     _       \n");
    console_write(" |  _ \\  __ _ _ __| | ___ __   ___   __| | ___  \n");
    console_write(" | | | |/ _` | '__| |/ / '_ \\ / _ \\ / _` |/ _ \\ \n");
    console_write(" | |_| | (_| | |  |   <| | | | (_) | (_| |  __/ \n");
    console_write(" |____/ \\__,_|_|  |_|\\_\\_| |_|\\___/ \\__,_|\\___| \n");
    console_write("\n");

    console_set_color(DN_COLOR_HEADER, DN_COLOR_BG);
    console_write("  " DARKNODE_NAME " ");
    console_set_color(DN_COLOR_DIM, DN_COLOR_BG);
    console_write("v" DARKNODE_VERSION " | ");
    console_write(DARKNODE_YEAR);
    console_write(" | ");
    console_write(DARKNODE_AUTHOR);
    console_write("\n\n");
    console_set_color(DN_COLOR_FG, DN_COLOR_BG);
}

static void boot_log(const char *component, const char *status) {
    console_write("  [");
    console_write_color("OK", DN_COLOR_OK);
    console_write("] ");
    console_write(component);
    if (status) {
        console_write_color(" — ", DN_COLOR_DIM);
        console_write_color(status, DN_COLOR_DIM);
    }
    console_write("\n");
}

void kmain(uint32_t magic, multiboot2_info_t *mbi) {
    console_init();
    serial_init();
    serial_write("[darknode] booting...\n");

    boot_banner();

    gdt_init();
    boot_log("GDT", "5 segments (null, kcode, kdata, ucode, udata)");

    idt_init();
    boot_log("IDT", "256 gates, PIC remapped");

    timer_init(1000);
    boot_log("PIT", "1000 Hz system timer");

    keyboard_init();
    boot_log("PS/2 Keyboard", "scancode set 1");

    rtc_init();
    boot_log("RTC", "real-time clock");

    if (magic == MULTIBOOT2_MAGIC) {
        pmm_init(mbi);
        char buf[32];
        utoa(pmm_total_memory(), buf, 10);
        boot_log("PMM", buf);
        console_write("         ");
        console_write_dec(pmm_total_memory() / 1024);
        console_write(" MiB total, ");
        console_write_dec(pmm_free_pages());
        console_write(" free pages\n");
    } else {
        console_write_color("  [!!] ", DN_COLOR_ERR);
        console_write("multiboot2 magic mismatch — PMM skipped\n");
    }

    heap_init();
    boot_log("Heap", "4 MiB kernel heap at 0x400000");

    pci_init();
    char pcibuf[16];
    itoa(pci_device_count(), pcibuf, 10);
    strcat(pcibuf, " devices found");
    boot_log("PCI", pcibuf);

    __asm__ volatile("sti");
    boot_log("Interrupts", "enabled");

    console_write("\n");
    console_write_color("  Type 'help' for available commands.\n\n", DN_COLOR_DIM);

    serial_write("[darknode] boot complete, entering shell\n");

    shell_init();
    shell_run();
}
