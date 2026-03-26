document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('ripetente').addEventListener('change', function () {
        document.getElementById('numeriField').classList.toggle('active', this.checked);
        document.getElementById('anniRipetuti').value = '';
    });
    
    document.getElementById('registrationForm').addEventListener('submit', function (e) {
        e.preventDefault();
        document.getElementById('errorContainer').classList.remove('show');
        
        var errors = [];
        var dati = {};
        
        // Valida Nome
        var nome = document.getElementById('nome').value.trim();
        if (!nome || nome.length < 2) {
            errors.push("Nome: almeno 2 caratteri");
            document.getElementById('nome').classList.add('error');
        } else {
            dati.nome = nome;
            document.getElementById('nome').classList.remove('error');
        }
        
        // Valida Cognome
        var cognome = document.getElementById('cognome').value.trim();
        if (!cognome || cognome.length < 2) {
            errors.push("Cognome: almeno 2 caratteri");
            document.getElementById('cognome').classList.add('error');
        } else {
            dati.cognome = cognome;
            document.getElementById('cognome').classList.remove('error');
        }
        
        // Valida Data Nascita
        var data = document.getElementById('dataNascita').value;
        var dateObj = new Date(data);
        var eta = new Date().getFullYear() - dateObj.getFullYear();
        if (!data || eta < 14) {
            errors.push("Data di Nascita: deve avere almeno 14 anni");
            document.getElementById('dataNascita').classList.add('error');
        } else {
            dati.dataNascita = data;
            document.getElementById('dataNascita').classList.remove('error');
        }
        
        // Valida Codice Fiscale
        var cf = document.getElementById('codiceFiscale').value.toUpperCase();
        if (!cf || cf.length !== 16 || !/^[A-Z]{6}[0-9]{2}[A-Z][0-9]{2}[A-Z][0-9]{3}[A-Z]$/.test(cf)) {
            errors.push("Codice Fiscale: formato non valido");
            document.getElementById('codiceFiscale').classList.add('error');
        } else {
            dati.codiceFiscale = cf;
            document.getElementById('codiceFiscale').classList.remove('error');
        }
        
        // Valida Classe
        var classe = document.getElementById('classe').value;
        if (!classe) {
            errors.push("Classe: selezionare una classe");
            document.getElementById('classe').classList.add('error');
        } else {
            dati.classe = classe;
            document.getElementById('classe').classList.remove('error');
        }
        
        // Valida Sezione
        var sezione = document.getElementById('sezione').value;
        if (!sezione) {
            errors.push("Sezione: selezionare una sezione");
            document.getElementById('sezione').classList.add('error');
        } else {
            dati.sezione = sezione;
            document.getElementById('sezione').classList.remove('error');
        }
        
        // Valida Ripetente e Anni
        var ripetente = document.getElementById('ripetente').checked;
        dati.ripetente = ripetente;
        if (ripetente) {
            var anni = document.getElementById('anniRipetuti').value;
            if (!anni || anni < 1 || anni > 3) {
                errors.push("Anni Ripetuti: numero tra 1 e 3");
                document.getElementById('anniRipetuti').classList.add('error');
            } else {
                dati.anniRipetuti = parseInt(anni);
                document.getElementById('anniRipetuti').classList.remove('error');
            }
        } else {
            dati.anniRipetuti = 0;
        }
        
        // Valida Uscita
        var uscita = document.getElementById('uscita').value;
        if (!uscita) {
            errors.push("Sbocco: selezionare un'opzione");
            document.getElementById('uscita').classList.add('error');
        } else {
            dati.uscita = uscita;
            document.getElementById('uscita').classList.remove('error');
        }
        
        // Mostra errori o salva
        if (errors.length > 0) {
            var errorList = document.getElementById('errorList');
            errorList.innerHTML = errors.map(e => '<li class="error-item">✗ ' + e + '</li>').join('');
            document.getElementById('errorContainer').classList.add('show');
        } else {
            localStorage.setItem('studentData', JSON.stringify(dati));
            window.location.href = 'risultati.html';
        }
    });
});
