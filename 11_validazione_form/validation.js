document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('ripetente').addEventListener('change', function() {
        document.getElementById('anniField').classList.toggle('active');
    });
    
    document.getElementById('form').addEventListener('submit', function(e) {
        e.preventDefault();
        
        var campi = {
            nome: 'nome',
            cognome: 'cognome',
            data: 'data',
            cf: 'cf',
            classe: 'classe',
            sezione: 'sezione',
            sbocco: 'sbocco',
            anni: 'anni'
        };
        
        var errori = [];
        var dati = {};
        
        // Pulisci errori precedenti
        Object.keys(campi).forEach(function(key) {
            document.getElementById(campi[key]).classList.remove('error');
        });
        
        // Valida Nome
        var nome = document.getElementById('nome').value.trim();
        if (!nome || nome.length < 2) {
            errori.push('Nome: minimo 2 caratteri');
            document.getElementById('nome').classList.add('error');
        } else {
            dati.nome = nome;
        }
        
        // Valida Cognome
        var cognome = document.getElementById('cognome').value.trim();
        if (!cognome || cognome.length < 2) {
            errori.push('Cognome: minimo 2 caratteri');
            document.getElementById('cognome').classList.add('error');
        } else {
            dati.cognome = cognome;
        }
        
        // Valida Data (almeno 14 anni)
        var data = document.getElementById('data').value;
        if (!data) {
            errori.push('Data: obbligatoria');
            document.getElementById('data').classList.add('error');
        } else {
            var eta = new Date().getFullYear() - new Date(data).getFullYear();
            if (eta < 14) {
                errori.push('Data: deve avere almeno 14 anni');
                document.getElementById('data').classList.add('error');
            } else {
                dati.dataNascita = data;
            }
        }
        
        // Valida Codice Fiscale
        var cf = document.getElementById('cf').value.toUpperCase();
        if (!cf || cf.length !== 16 || !/^[A-Z]{6}[0-9]{2}[A-Z][0-9]{2}[A-Z][0-9]{3}[A-Z]$/.test(cf)) {
            errori.push('Codice Fiscale: formato non valido');
            document.getElementById('cf').classList.add('error');
        } else {
            dati.codiceFiscale = cf;
        }
        
        // Valida Classe
        var classe = document.getElementById('classe').value;
        if (!classe) {
            errori.push('Classe: obbligatoria');
            document.getElementById('classe').classList.add('error');
        } else {
            dati.classe = classe;
        }
        
        // Valida Sezione
        var sezione = document.getElementById('sezione').value;
        if (!sezione) {
            errori.push('Sezione: obbligatoria');
            document.getElementById('sezione').classList.add('error');
        } else {
            dati.sezione = sezione;
        }
        
        // Valida Ripetente
        var ripetente = document.getElementById('ripetente').checked;
        dati.ripetente = ripetente;
        
        if (ripetente) {
            var anni = document.getElementById('anni').value;
            if (!anni || anni < 1 || anni > 3) {
                errori.push('Anni Ripetuti: numero tra 1 e 3');
                document.getElementById('anni').classList.add('error');
            } else {
                dati.anniRipetuti = parseInt(anni);
            }
        }
        
        // Valida Sbocco
        var sbocco = document.getElementById('sbocco').value;
        if (!sbocco) {
            errori.push('Sbocco Professionale: obbligatorio');
            document.getElementById('sbocco').classList.add('error');
        } else {
            dati.sbocco = sbocco;
        }
        
        // Mostra errori o salva
        var containerErrori = document.getElementById('errori');
        if (errori.length > 0) {
            var html = errori.map(function(e) {
                return '<div class="error-item">✗ ' + e + '</div>';
            }).join('');
            document.getElementById('listaErrori').innerHTML = html;
            containerErrori.classList.add('show');
        } else {
            localStorage.setItem('dati', JSON.stringify(dati));
            window.location.href = 'risultati.html';
        }
    });
});
