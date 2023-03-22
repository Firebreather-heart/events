const speaker = document.querySelector('#item1');
const partner = document.querySelector('#item2');
var splus = document.querySelectorAll('#sneaky-s');
var pplus = document.querySelectorAll('#sneaky-p');

for (var i = 0; i < pplus.length; i++){
    pplus[i].style.display = 'none';
}

speaker.classList.add('active', 'w3-text-white');
partner.classList.add('w3-grey');

const selectSp = () => {
    if (speaker.classList.contains('active'))
    {
        speaker.classList.remove('active', 'w3-text-white',);
        speaker.classList.add('w3-grey');
        partner.classList.add('active', 'w3-text-white',);
        partner.classList.remove('w3-grey');
        for (var i = 0; i < pplus.length; i++) {
            pplus[i].style.display = 'block';
            splus[i].style.display = 'none';
        }
    }
    else if (partner.classList.contains('active'))
    {
        partner.classList.remove('active', 'w3-text-white');
        partner.classList.add('w3-grey');
        speaker.classList.add('active', 'w3-text-white');
        speaker.classList.remove('w3-grey');
        for (var i = 0; i < pplus.length; i++) {
            pplus[i].style.display = 'none';
            splus[i].style.display = 'block';
        }
        }
} 