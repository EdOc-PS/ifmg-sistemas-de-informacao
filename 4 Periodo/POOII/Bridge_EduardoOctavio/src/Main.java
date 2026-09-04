public class Main
{

    public static void main(String[] aaaaaaaaaaaaaaaaaaa){
        ControleRemoto tv1 = new TvQueFicaMuda(new TV(1,100));
        ControleRemoto tv2 = new TvQuePausa(new TV(1,200));
        ControleRemoto play = new PlayStation2(new Playstation(1, 1));
        ControleRemoto blueRay = new BlueRay_Sony(new BlueRay (1, 1));
        
        System.out.println("Testando a TV que fica muda:");
        tv1.botaoCinco();
        tv1.botaoSeis();
        tv1.botaoNove();
        System.out.println();
        
        System.out.println("Testando a TV que pausa:");
        tv2.botaoCinco();
        tv2.botaoSeis();
        tv2.botaoNove();
        System.out.println();
        
        System.out.println("Testando o controle do PlayStation:");
        play.botaoCinco();
        play.botaoSeis();
        play.botaoNove();
        System.out.println();
        
        System.out.println("Testando o controle do BlueRay:");
        blueRay.botaoCinco();
        blueRay.botaoSeis();
        blueRay.botaoNove();
    
    }

}
