console.log('forms/chunk_upload.js')

// capture submit
const form = document.querySelector('form')


// dz2 = new DropZone()
// dz2.setup({
//     dropSpace: '.single.drag-drop-zone'
//     , formField: '#id_file'
// })

const formSubmitHandler = function(ev) {
    // ev.stopImmediatePropagation()
    // ev.stopPropagation()
    ev.preventDefault()
    console.log('Stop')

    // get origin form
    // delete files
    // post for pre-fetch
    let form = ev.currentTarget
    let formData = new FormData(form)
    let files = formData.getAll('file')
    formData.delete('file')

    // Install the byte size
    let size = countBytesMany(files)
    setFileField(form, formData, 'byte_size', size)

    // Populate the real filename if required.
    let name = formData.get('filename')
    let f = files[0]
    let realName = f.name

    setFileField(form, formData, 'filetype', f.type)
    setFileField(form, formData, 'filepath', realName)

    if(name.length == 0) {
        // setFileField(form, formData, 'filename', realName)
        formData.set('filename', realName)
    }

    return fetch(form.action, {
            method: 'POST',
            body: formData,
            // body: stream(formData),
            // headers: {'Content-Type': 'text/plain'},
            // duplex: 'half',
        })
        .then((response) => response.json())
        .then(function(d){
            document.querySelector('.merge-link').dataset.uuid = d.file_uuid
            let eachFunc = function(d){
                console.log('eachFunc', d)
                d.timeTaken
            }
            return submitParts(form, d, eachFunc)
        })
}


form.addEventListener('submit', formSubmitHandler)


const openFormMerge = function(ev) {
    let uuid = ev.currentTarget.dataset.uuid
    if(uuid == undefined) {
        console.warn('File not given')
        return
    }
    // let url = `/corsa/upload/merge/${uuid}/`
    let url = getMergeURL(uuid)
    window.location = url;
}

const getMergeURL = function(value){
    return UPLOADS['mergeView'].replace(UPLOADS['templateStr'], value)
    // let url = `/corsa/upload/merge/${uuid}/`
}


const setFileField = function(form, formData, key, value, fieldname) {
    if(fieldname == undefined) {
        fieldname = key
    }
    formData.set(key, value)
    form.querySelector(`[name='${fieldname}']`).value = value;
}


const countBytesMany = function(files) {
    let numberOfBytes = 0;

    for(let file of files) {
        numberOfBytes += countBytes(file)
    }
    return numberOfBytes
}


const countBytes = function(file) {
    return file.size;
}


const chunkSize = 1024 * 1024; // size of each chunk (1MB)
const submitParts = function(form, extra, eachFunc){
    // Read the file
    // make a new form to the parts endpoint.
    let formData = new FormData(form)
    let files = formData.getAll('file')

    for(let file of files) {
        submitFileForm(file, extra, (x) => allDoneFunc(form, x), eachFunc)
    }
}

const allDoneFunc = function(form, file){
    console.log('Done', form, file)
}

const progressBar = function(){
    return document.querySelector('#file_upload_progress')
}


const progressBarLabel = function(){
    return document.querySelector('.upload_percent .percent-text')
}


const submitFileForm = function(file, extra, allDoneFunc, eachFunc) {
    let doneCount = 0;
    let pc = Math.ceil(file.size / chunkSize)

    let pg = progressBar()
    let pgl = progressBarLabel()
    let eachCache = { timeIn: +(new Date) }

    let _eachFunc = function(d){
        doneCount += 1
        let v = (doneCount/pc) * 100
        console.log('Total', `${doneCount}/${pc} - ${v}`, d)
        pg.value = v;
        pgl.innerText = `${v.toFixed(0)}%`
        let r = Object.assign({}, d, {
                    index: doneCount,
                    percent: v,
                    file,
                    extra,
                    timeTaken: +(new Date) - eachCache.timeIn
                })
        eachFunc && eachFunc(r)
        eachCache.timeIn = +(new Date)
    }

    let _allDoneFunc = function(d) {
        let r = Object.assign({}, d, {timeTaken: +(new Date) - eachCache.timeIn})
        allDoneFunc && allDoneFunc(r)

    }

    console.log(getSize(file), pc, 'chunks')
    // let sent = chunkFileUpload(file, extra, _eachFunc)
    let sent = chunkFileUploadLinear(file, extra, _eachFunc, _allDoneFunc)
    console.log('sent', sizeString(sent))

}


const getSize = function(file) {
    // Calculate total size
    // let numberOfBytes = 0;
    let  numberOfBytes = countBytes(file)
    // for (const file of uploadInput.files) {
    //   numberOfBytes += file.size;
    // }
    return sizeString(numberOfBytes)
}


const sizeString = function(numberOfBytes){
    // Approximate to the closest prefixed unit
    const units = [
        "B",
        "KiB",
        "MiB",
        "GiB",
        "TiB",
        "PiB",
        "EiB",
        "ZiB",
        "YiB",
    ];

    const exponent = Math.min(
        Math.floor(Math.log(numberOfBytes) / Math.log(1024)),
        units.length - 1,
    );

    const approx = numberOfBytes / 1024 ** exponent;

    if(exponent === 0) {
        return `${numberOfBytes} bytes`
    }

    let s = `${approx.toFixed(3)} ${units[exponent]} (${numberOfBytes} bytes)`;
    return s
}


function chunkFileUpload(file, extra, eachFunc, allDoneFunc) {

    let start = 0;
    let index = 0
    let bits = file.slice(start, start + chunkSize);

    let partResponseHandler = eachFunc || function(a){ return a }
    let promises = [];

    while (start < file.size) {
        let _extra = {
                file_uuid: extra.file_uuid,
                chunk_index: index,
            }
        let fetchPromise = uploadChunk(bits, _extra)
                            .then((response)=> response.json())
                            .then(partResponseHandler)
                            ;

        promises.push(fetchPromise)
        start += chunkSize
        index++;
    }

    Promise.all(promises).then((values)=> {
        console.log('All Done')
        allDoneFunc && allDoneFunc(values)
    })
    return start
}


function chunkFileUploadLinear(file, extra, chunkHandler, doneHandler) {
    return chunkFileUploadLinearLoop(file, extra, 0, 0, chunkHandler, doneHandler)
}


function chunkFileUploadLinearLoop(file, extra, index=0, start=0, chunkHandler=undefined, doneHandler=undefined) {

    if(start > file.size) {
        // no more to push.
        console.log('done')
        return doneHandler && doneHandler(file)
    }

    let innerChunkHandler = (r)=>{
            let v = Object.assign(r, { chunkSize: chunkSize })
            chunkHandler && chunkHandler(v);
            return r
        }

    let loopHandler = function(){
            let v = index + 1;
            let newExtra = Object.assign({}, extra, { index: v})
            return chunkFileUploadLinearLoop(file, newExtra, v, newStart,
                                             chunkHandler, doneHandler)
        }

    let newStart = start + chunkSize;
    let bits = file.slice(start, newStart);
    let newExtra = Object.assign({}, extra, { index })
    let chunkPromise = sendChunk(bits, newExtra)
                            .then(innerChunkHandler)
                            .then(loopHandler)
                            ;

    return chunkPromise;
}


function sendChunk(bits, extra){

    let _extra = {
            file_uuid: extra.file_uuid,
            chunk_index: extra.index,
        }

    let fetchPromise = uploadChunk(bits, _extra)
                        .then((response)=> response.json())
                        ;
    // return start
    return fetchPromise
}


function uploadChunk(chunk, extra) {
    let uploadForm = document.querySelector('.file-chunk-form form')
    let formUrl = uploadForm.action
    const formData = new FormData(uploadForm);

    let index = extra.chunk_index
    for(let k in extra) {
        // console.log('Appending', k)
        let v = extra[k]
        formData.append(k, v)
        setFileField(uploadForm, formData, k, v)
    }

    formData.append('filepart', chunk)

    console.log('Sending Chunk', index);
    // Make a request to the server
    return fetch(`${formUrl}${index}/`, {
        method: 'POST',
        body: formData,
        // body: stream(formData),
        // headers: {'Content-Type': 'text/plain'},
        // duplex: 'half',
    });
}




function wait(milliseconds) {
    return new Promise(resolve => setTimeout(resolve, milliseconds));
}


var stream = function(formData) {

    return new ReadableStream({
    // const rstream = new ReadableStream({
      async start(controller) {
        // await wait(1000);
        // debugger
        controller.enqueue(formData);
        // await wait(1000);
        // controller.enqueue('is ');
        // await wait(1000);
        // controller.enqueue('a ');
        // await wait(1000);
        // controller.enqueue('slow ');
        // await wait(1000);
        // controller.enqueue('request.');
        controller.close();
      },
    })//.pipeThrough(new TextEncoderStream());
}

