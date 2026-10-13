from operator import attrgetter



class Strumento:
    def __init__(self, id_strumento, tipo, marca, anno, valore):
        self.id_strumento = id_strumento
        self.tipo = tipo
        self.marca = marca
        self.anno = anno
        self.valore = valore

    def __str__(self):
        return self.id_strumento + ", " + self.tipo + " " + self.marca + " (" + str(self.anno) + ") - " + str(
            self.valore) + " euro"


class Prestito:
    def __init__(self, id_prestito, data, id_strumento, cognome_allievo):
        self.id_prestito = id_prestito
        self.data = data
        self.id_strumento = id_strumento
        self.cognome_allievo = cognome_allievo

    def __str__(self):
        return self.id_prestito + " - Strumento: " + self.id_strumento + " - Allievo: " + self.cognome_allievo


class DepositoStrumenti:
    def __init__(self, nome, responsabile):
        """Inizializza gli attributi e le strutture dati"""
        self.nome = nome
        self.responsabile = responsabile
        self.strumenti = []
        self.prestiti = []

        # Variabili di appoggio per calcolare i codici univoci in automatico
        self.ultimo_id_strumento = 0
        self.ultimo_id_prestito = 0

    def carica_file_strumenti(self, file_path):
        """Carica gli strumenti dal file"""
        try:
            f = open(file_path, "r", encoding="utf-8")
            for riga in f:
                campi = riga.strip().split(",")
                if len(campi) < 5:
                    continue

                id_strum = campi[0].strip()
                tipo = campi[1].strip()
                marca = campi[2].strip()
                anno = int(campi[3])
                valore = float(campi[4])

                # Calcolo il numero dell'ID togliendo la "S" iniziale per tenere il conto
                numero_id = int(id_strum[1:])
                if numero_id > self.ultimo_id_strumento:
                    self.ultimo_id_strumento = numero_id

                nuovo_strumento = Strumento(id_strum, tipo, marca, anno, valore)
                self.strumenti.append(nuovo_strumento)

            f.close()
        except FileNotFoundError:
            raise FileNotFoundError("Errore: file non trovato.")

    def aggiungi_strumento(self, tipo, marca, anno_acquisto, valore):
        """Aggiunge uno strumento nel deposito: aggiunge solo nel sistema e non aggiorna il file"""
        self.ultimo_id_strumento = self.ultimo_id_strumento + 1
        nuovo_codice = "S" + str(self.ultimo_id_strumento)

        nuovo_strumento = Strumento(nuovo_codice, tipo, marca, anno_acquisto, valore)
        self.strumenti.append(nuovo_strumento)

        return nuovo_strumento

    def strumenti_ordinati_per_marca(self):
        """Ordina gli strumenti per marca in ordine alfabetico"""
        # Uso attrgetter come suggerito dalla traccia
        lista_ordinata = sorted(self.strumenti, key=attrgetter("marca"))
        return lista_ordinata

    def nuovo_prestito(self, data, id_strumento, cognome_allievo):
        """Crea un nuovo prestito"""
        # 1. Controllo se lo strumento esiste nel sistema
        strumento_trovato = False
        for s in self.strumenti:
            if s.id_strumento == id_strumento:
                strumento_trovato = True

        if strumento_trovato == False:
            raise Exception("Errore: lo strumento richiesto non esiste nel deposito.")

        # 2. Controllo se lo strumento è già in prestito a qualcun altro
        for p in self.prestiti:
            if p.id_strumento == id_strumento:
                raise Exception("Errore: lo strumento è già attualmente in prestito.")

        # 3. Creo il nuovo prestito
        self.ultimo_id_prestito = self.ultimo_id_prestito + 1
        codice_prestito = "P" + str(self.ultimo_id_prestito)

        nuovo_p = Prestito(codice_prestito, data, id_strumento, cognome_allievo)
        self.prestiti.append(nuovo_p)

        return nuovo_p

    def termina_prestito(self, id_prestito):
        """Termina un prestito in atto"""
        trovato = False
        for p in self.prestiti:
            if p.id_prestito == id_prestito:
                self.prestiti.remove(p)
                trovato = True

        if trovato == False:
            raise Exception("Errore: codice prestito non trovato.")