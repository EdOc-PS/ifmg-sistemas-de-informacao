/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */

/**
 *
 * @author eeuar
 */
public class BlueRay_Sony extends ControleRemoto{

    public BlueRay_Sony(Dispositivo novo_) {
        super(novo_);
    }

    @Override
    public void botaoNove() {
        System.out.println("Ejetando o disco");
    }
    
}
