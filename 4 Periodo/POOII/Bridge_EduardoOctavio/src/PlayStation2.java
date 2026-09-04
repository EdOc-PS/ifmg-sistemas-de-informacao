/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */

/**
 *
 * @author eeuar
 */
public class PlayStation2 extends ControleRemoto{

    public PlayStation2(Dispositivo novo_) {
        super(novo_);
    }

    @Override
    public void botaoNove() {
        System.out.println("Abrindo a tampa...");
    }
    
}
