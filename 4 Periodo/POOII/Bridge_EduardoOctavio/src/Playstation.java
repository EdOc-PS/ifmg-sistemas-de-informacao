/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */

/**
 *
 * @author eeuar
 */
public class Playstation extends Dispositivo {

    public Playstation(int estado_, int maximo_) {
        estado = estado_;
        maximo = maximo_;
    }

    @Override
    public void botaoCinco() {
        System.out.println("Ligando o Play.");
    }

    @Override
    public void botaoSeis() {
        System.out.println("Iniciando o jogo");
    }

}
