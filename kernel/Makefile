# Darknode OS — Kernel Build System
# Requires: nasm, i686-elf-gcc (or gcc -m32), grub-mkrescue, xorriso

CC      = i686-elf-gcc
AS      = nasm
LD      = i686-elf-ld
CFLAGS  = -m32 -std=gnu99 -ffreestanding -O2 -Wall -Wextra -Iinclude -Ikernel -Idrivers
ASFLAGS = -f elf32
LDFLAGS = -T linker.ld -nostdlib

# Fallback to system gcc if cross-compiler not found
ifeq ($(shell which $(CC) 2>/dev/null),)
CC = gcc
LD = ld
endif

KERNEL = darknode.elf
ISO    = darknode-os.iso

ASM_SRCS = boot/multiboot.asm boot/boot.asm boot/gdt.asm boot/idt.asm
C_SRCS   = kernel/kernel.c kernel/console.c kernel/string.c kernel/gdt.c \
           kernel/idt.c kernel/timer.c kernel/keyboard.c kernel/pmm.c \
           kernel/heap.c kernel/serial.c kernel/shell.c \
           drivers/rtc.c drivers/pci.c

ASM_OBJS = $(ASM_SRCS:.asm=.o)
C_OBJS   = $(C_SRCS:.c=.o)
OBJS     = $(ASM_OBJS) $(C_OBJS)

.PHONY: all clean iso run debug

all: $(KERNEL)

$(KERNEL): $(OBJS)
	$(LD) $(LDFLAGS) -o $@ $^

%.o: %.asm
	$(AS) $(ASFLAGS) -o $@ $<

%.o: %.c
	$(CC) $(CFLAGS) -c -o $@ $<

iso: $(KERNEL)
	mkdir -p isodir/boot/grub
	cp $(KERNEL) isodir/boot/darknode.elf
	echo 'set timeout=0'                    >  isodir/boot/grub/grub.cfg
	echo 'set default=0'                    >> isodir/boot/grub/grub.cfg
	echo 'menuentry "Darknode OS" {'        >> isodir/boot/grub/grub.cfg
	echo '    multiboot2 /boot/darknode.elf' >> isodir/boot/grub/grub.cfg
	echo '    boot'                          >> isodir/boot/grub/grub.cfg
	echo '}'                                 >> isodir/boot/grub/grub.cfg
	grub-mkrescue -o $(ISO) isodir
	@echo "\n  $(ISO) ready — boot with: qemu-system-i386 -cdrom $(ISO)\n"

run: iso
	qemu-system-i386 -cdrom $(ISO) -serial stdio -m 128M

debug: iso
	qemu-system-i386 -cdrom $(ISO) -serial stdio -m 128M -s -S

clean:
	rm -f $(OBJS) $(KERNEL) $(ISO)
	rm -rf isodir
