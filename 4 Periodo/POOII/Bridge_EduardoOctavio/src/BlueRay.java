/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */

/**
 *
 * @author eeuar
 */
public class BlueRay extends Dispositivo {

    public BlueRay(int estado_, int maximo_) {
        estado = estado_;
        maximo = maximo_;
    }

    @Override
    public void botaoCinco() {
        System.out.println("Ligando o BlueRay.");
    }

    @Override
    public void botaoSeis() {
        System.out.println("Pausando o BlueRay");
    }

}
