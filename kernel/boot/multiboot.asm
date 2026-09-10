; Multiboot2 header — must appear in the first 32 KiB of the binary.
section .multiboot
align 8

mb2_start:
    dd 0xe85250d6            ; magic
    dd 0                     ; architecture: i386
    dd mb2_end - mb2_start   ; header length
    dd -(0xe85250d6 + 0 + (mb2_end - mb2_start)) ; checksum

    ; end tag
    dw 0    ; type
    dw 0    ; flags
    dd 8    ; size
mb2_end:
