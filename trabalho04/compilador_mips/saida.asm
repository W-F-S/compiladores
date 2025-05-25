.data
var_a: .word 0
var_b: .word 0
.text
.globl main
main:
li $t0, 5
sw $t0, var_a
lw $t0, var_a
sw $t0, 0($sp)
addi $sp, $sp, -4
li $t0, 3
addi $sp, $sp, 4
lw $t1, 0($sp)
add $t0, $t1, $t0
sw $t0, var_b
lw $a0, var_b
li $v0, 1
syscall
li $v0, 10
syscall