import matplotlib.pyplot as plt


# questa funzione può essere utilizzata per tutti i tipi di AI, eventualmente aggiungo un parametro che in base al tipo
# di IA cambia la tipologia di grafico da disegnare
def plot_results(scoreArray, game_index_array, w0, w1, w2, w3):
    plt.figure(1)  # crea la finestra in cui stampare i grafici
    plt.subplot(211)  # descrive la posizione dei subplot, con 211 si riferisce al grafico che sta in alto
    plt.plot(game_index_array, scoreArray, 'k-')  # disegna il grafico utilizzando i parametri che gli vengono passati
    plt.xlabel('Game Number')  # assegna un nome all'asse delle x
    plt.ylabel('Game Score')  # assegna un nome all'asse delle y
    plt.title('Learning Curve')  # titolo del grafico che sta in alto
    plt.xlim(1, max(game_index_array))  # definisce il valore minimo e il valore massimo che l'asse delle x dovrà avere
    plt.ylim(0, max(scoreArray) * 1.1)  # definisce il valore minimo e il valore massimo che l'asse delle y dovrà avere

    # disegna il grafico dei pesi man mano
    plt.subplot(212)  # descrive la posizione dei subplot, con 212 si riferisce al grafico che sta in basso
    plt.xlabel('Game Number')  # nome dell'asse delle x
    plt.ylabel('Weights')  # nome dell'asse delle y
    plt.title('Learning Curve')  # titolo delle secondo grafico
    ax = plt.gca()  # restituisce gli assi del grafico creato precedentemente
    ax.set_yscale('log')  # serve per settare lo scaling delle y, in questo caso è logaritmico
    plt.plot(game_index_array, w0, label="Aggregate Height")  # funzione che mostra l'andamento dei pesi aggregati
    plt.plot(game_index_array, w1, label="Unevenness")  # funzione che mostra l'andamento dell'unevenness
    plt.plot(game_index_array, w2, label="Maximum Height")  # funzione che mostra l'andamento dell'altezza massima
    plt.plot(game_index_array, w3, label="Number of Holes")  # funzione che mostra l'andamento del numero di buchi
    plt.legend(loc='lower left')  # pone la legenda in basso a sinistra
    plt.xlim(0, max(game_index_array))  # definisce il valore minimo e il valore massimo che l'asse delle x dovrà avere
    plt.ylim(0.0001, 100)  # definisce il valore minimo e il valore massimo che l'asse delle y dovrà avere
    plt.show()  # stampa a schermo i grafici
