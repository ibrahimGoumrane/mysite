const progressBar = document.getElementById('progress-bar');
const submitButton = document.querySelector('.imgsubmit');
const spinner = document.querySelector('#loading-spinner');
const form = document.querySelector('form');
const Class = document.querySelectorAll('.sec');
const cycle = document.querySelector('#cycle');
const cyclePrepa = document.querySelector('#cycle_prep');
const cycleEng = document.querySelector('#cycle_eng');
const module = document.querySelector('#module');
const cycleFiliere = document.querySelector('#cycle_fil');
const cycleSection = document.querySelector('#cycle_sec');
const filename = document.querySelector('#file-input');
const btnFile = document.querySelector('#file');
const fileLabel = document.querySelector('.section .mainform form > div:nth-child(7) label');
fileLabel.removeAttribute('for');
const init_span = function () {
    const fileName = document.querySelector('.file-name-label');
    if (fileName) {
        fileName.remove();
    }
}
filename.addEventListener('change', function () {
    init_span()
    const fileName = document.createElement('span');
    [...this.files].forEach((file) => {
        fileName.textContent += file.name;
    })
    fileName.classList.add('file-name-label');
    fileLabel.insertAdjacentElement("afterend", fileName);
})
btnFile.addEventListener('click', () => {
    filename.click();
})
function showLoadingIndicator() {
    spinner.style.display = 'block';
}

function hideLoadingIndicator() {
    spinner.style.display = 'none';
}
// function getFormData() {
//     const formData = new FormData();

//     // Iterate over form elements
//     for (const element of form.elements) {
//         // Skip elements without name attribute or non-input elements
//         if (!element.name || !['INPUT', 'SELECT', 'TEXTAREA'].includes(element.tagName)) {
//             continue;
//         }

//         // Handle file inputs separately
//         if (element.type === 'file') {
//             const files = element.files;
//             if (files.length > 0) {
//                 // Append each file to the FormData object
//                 for (const file of files) {
//                     formData.append(element.name, file);
//                 }
//             }
//         } else if (element.type === 'checkbox') {
//             formData.append(element.name, element.checked);
//         } else if (element.type === 'radio') {
//             if (element.checked) {
//                 formData.append(element.name, element.value);
//             }
//         } else {
//             formData.append(element.name, element.value);
//         }
//     }

//     return formData;
// }
const studentPresenceList = function (presenceData) {

}
function getCSRFToken() {
    console.log(document.cookie
        .split('; '));
    const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        .split('=')[1];
    return cookieValue;
}
getCSRFToken()
form.addEventListener('submit', function (e) {
    e.preventDefault();
    const csrfToken = getCSRFToken();
    // updateProgress()
    showLoadingIndicator();
    // Serialize form data
    const headers = new Headers();
    // headers.append('X-CSRFToken', csrfToken);
    // headers.append('Accept', 'application/json');
    // headers.append('Content-Type', 'multipart/form-data');

    const formData = new FormData(form);
    // for (const entry of formData.entries()) {
    //     console.log(entry);
    // }
    const options = {
        method: 'POST',
        body: formData,
        headers: headers,
    };
    fetch('/face_recognizer/', options).then(response => {
        if (!response.ok) {
            throw new Error('Failed to submit form');
        }
        // Hide the loading spinner when the server responds
        hideLoadingIndicator();
        // window.open('/thankyou/', '_blank');
        return response.text();

    })
        .then(data => {
            // Handle the server response if needed
            // Manipulate and use the HTML content
            // Find the element where you want to insert the HTML content
            const roothtml = document.querySelector('html');
            // Insert the parsed HTML content into the target element
            roothtml.innerHTML = data;

        })
        .catch(error => {
            console.error(error);
            // Hide the loading spinner in case of an error
        });
})
const init_modules = function () {
    console.log([...module.childNodes]);
    [...module.childNodes].forEach((element) => {
        element.remove();
    });
}
const dataVerification = function () {
    cycSended = null;
    cycYearSended = null;
    cycFiliereSended = null;
    if (cycle.value == 'cycle_preparatoire') {
        if (!cyclePrepa.value) return null;
        if (!cycleSection.value) return null;
        cycYearSended = cyclePrepa.value;
        cycFiliereSended = cycleSection.value;
    }
    else {
        if (!cycleEng.value) return null;
        if (!cycleFiliere.value) return null;
        cycYearSended = cycleEng.value;
        cycFiliereSended = cycleFiliere.value;
    }
    cycSended = cycle.value;
    return [
        cycSended,
        cycYearSended,
        cycFiliereSended,
    ]
}
const sendPostForModules = async function (e) {
    init_modules()
    //values sended with the request to the backend
    const data = dataVerification()

    if (!data) {
        console.log('enter all values to be able to send the modules request');
        return;
    };


    let cycSended = data[0];
    let cycYearSended = data[1];
    let cycFiliereSended = data[2];


    //header init
    const csrfToken = getCSRFToken();
    const headers = new Headers();
    headers.append('X-CSRFToken', csrfToken);
    headers.append('Accept', 'application/json');

    //body init
    const sectionData = JSON.stringify({
        'cycle': cycSended,
        'cycleYear': cycYearSended,
        'cycleFiliere': cycFiliereSended,
    });
    //options for the fetch api
    const options = {
        method: 'POST',
        body: sectionData,
        headers: headers,
    };
    try {
        //fetch request
        const requestModules = await fetch('/face_recognizer/modules', options);
        const ModulesBody = await requestModules.json();
        const modules_sub = ModulesBody.modules
        console.log(modules_sub);
        const option = document.createElement('option');
        option.value = '';
        option.textContent = 'choose a module';
        module.insertAdjacentElement("beforeend", option);
        modules_sub.forEach(module_data => {
            const option = document.createElement('option');
            option.value = module_data;
            option.textContent = module_data.split('_').join(' ');
            module.insertAdjacentElement("beforeend", option);
        });
    }
    catch (err) {
        console.log('en error has occurred : ', err);
    } finally {
        console.log('the request-response cycle for modules has ended with success');
    }
}

Class.forEach((input) => {
    console.log(input);
    input.addEventListener('change', sendPostForModules);
})
