/*Apply a 'drag and drop' zone for a field- focusing on _django_ forms, but the
form appliance should work with any form field..

Step 0: You have a form with  a file field:

    <form>
        <input type=file></input>
    </form>

Step 1: Create a div to accept the file drop

    <div class="single drag-drop-zone">
    </div>

Step 2: Apply the Dropzone setup in your JS:

    dz = new DropZone()
    dz.setup({
        dropSpace: '.single.drag-drop-zone'
        , formField: '#id_file'
    })

    dz2 = new DropZone()
    dz2.setup({
        dropSpace: '.multi.drag-drop-zone'
        , formField: '#id_files_field'
    })

---

Upon a file drop the Dropzone handler will populate the form field.

 */

let stop = function(event) {
    event.stopPropagation();
    event.preventDefault();
}



class DropZone {
    /* Identifiy a space, some options and the upload form location */

    finishDropClass = 'dropzone-complete'
    dragClass = 'dragover'

    constructor() {
        this.dragging = false
        this.config = {
            documentWatch: true
            , clickThrough: false
        }
        this.files = []
    }

    setup(config) {
        Object.assign(this.config, config)
        this.prepareAll()
    }

    prepareAll() {
        // Setup the dnd listeners.
        var dropZones = document.querySelectorAll(this.config.dropSpace)
        for(let node of dropZones) {
            this.prepare(node)
        }

        if(this.config.documentWatch) {
            this.documentMonitor()
        }

        let clickClass = this.config.clickThrough? 'clickable': 'not-clickable'
        this.addDropNodeClass(clickClass)
    }

    prepare(node) {
        this.listenToNode(node)
        node.classList.add('dropzone-ready')
        // map from the filefield
        this.setupFileField(node)
    }

    setupFileField(node) {
        let field = this.formNode
        // Mutli-map
        this.multiple = field.multiple
        node.dataset.multiple = this.multiple
        let func = ['remove', 'add'][Number(this.multiple)]
        node.classList[func]('dropzone-multiple')
    }

    documentMonitor(node=document.body) {

        let create = function(name, func){
            node.addEventListener(name, func.bind(this), false);
        }.bind(this)

        node.classList.add('dropzone-listening')
        create('dragover', this.documentDragOver)
        create('dragleave', this.documentDragLeave)
        create('dragend', this.documentDragEnd)
    }

    documentDragOver(event) {
        this.addDropNodeClass('document-highlight')
    }

    addDropNodeClass(className, funcName='add'){
        for(let node of this.dropNodes) {
            node.classList[funcName](className)
        }
    }

    removeDropNodeClass(className){
        return this.addDropNodeClass(className, 'remove')
    }

    documentDragEnd(event) {
        this.removeDropNodeClass('document-highlight')
    }

    documentDragLeave(event) {
        this.removeDropNodeClass('document-highlight')
    }

    listenToNode(node){
        /*
            Event     Fires when...
            drag      ...a dragged item (element or text selection) is dragged.
            dragend   ...a drag operation ends (such as releasing a mouse
                         button or hitting the Esc key; see Finishing a Drag.)
            dragenter ...a dragged item enters a valid drop target.
                         (See Specifying Drop Targets.)
            dragleave ...a dragged item leaves a valid drop target.
            dragover  ...a dragged item is being dragged over a valid drop
                         target, every few hundred milliseconds.
            dragstart ...the user starts dragging an item.
                         (See Starting a Drag Operation.)
            drop      ...an item is dropped on a valid drop
                         target. (See Performing a Drop.)
        */
        let create = function(name, func){
            node.addEventListener(name, func.bind(this), false);
        }.bind(this)

        create('dragover', this.onDragOverEvent)
        create('dragleave', this.onDragLeaveEvent)
        create('drop', this.onDropEvent)
        create('dropend', this.onDropEndEvent)
        create('click', this.onClickEvent)

        node.classList.add('dropzone-listening')
    }

    onClickEvent(event) {
        if(this.config.clickThrough) {
            this.formNode.click(event)
            return
        }

        this.removeDropNodeClass('clicked')
        window.setTimeout(()=>this.addDropNodeClass('clicked'), 100)
    }

    onDropEndEvent(event) {
        console.log('onDropEndEvent', event)
        stop(event)
        this.stopDrag(event)
    }

    onDragLeaveEvent(event) {
        console.log('onDragLeaveEvent', event)
        stop(event)
        this.stopDrag(event)
    }

    stopDrag(event){
        this.dragging = false
        event.dataTransfer.dropEffect = ''; // Explicitly show this is a copy.
        event.target.classList.remove(this.dragClass)
        event.target.classList.remove('clicked')
    }

    readImage(f) {
        if (!f.type.match('image.*')) {
            return
          }

        var reader = new FileReader();

        // Closure to capture the file information.
        // reader.onload = (function(theFile) {
        //         return function(e) {
        //             // Render thumbnail.
        //             let src = e.target.result
        //             let escapedName = escape(theFile.name);
        //             `<img class="thumb" src="${src}" title="${escapedName}"/>`
        //         };
        //     })(f);

          // Read in the image file as a data URL.
          let dataUrl = reader.readAsDataURL(f);
          return dataUrl;
    }

    startDrag(event) {
        this.dragging = true
        event.dataTransfer.dropEffect = 'copy'; // Explicitly show this is a copy.
        let cl = event.target.classList
        cl.add(this.dragClass)
        cl.remove(this.finishDropClass)
    }

    onDragOverEvent(event) {
        stop(event)

        if(this.dragging) { return }

        console.log('onDragOverEvent', event)
        this.startDrag(event)
    }

    onDropEvent(event) {
        stop(event)
        console.log('onDropEvent', event)
        var files = event.dataTransfer.files; // FileList object.
        this.printFiles(files)
        // files is a FileList of File objects. List some properties.
        this.files = files
        this.stopDrag(event)
        this.pushFiles(this.files)
        console.log(this.dropZones)
        for(let node of this.dropNodes) {
            this.finishDrop(node)
        }
    }

    finishDrop(node) {
        node.classList.add(this.finishDropClass)
        node.dataset.count = this.files.length
    }

    pushFiles(files) {
        /* Send the file choices to the chosen form field and other actions */
        let formNode = this.getFormNodeField()
        formNode.files = this.files
    }

    getFormNodeField(){
        let fieldName = this.config.formField
        if(fieldName == undefined) {
            return
        }

        let field = document.querySelector(fieldName);

        if(field == null) {
            console.error('Given fieldName cannot be found', fieldName)
            return
        }

        return field
    }

    get formNode() {
        return this.getFormNodeField()
    }

    get dropNodes() {
        return this.getDropNodes()
    }

    getDropNodes() {
        return document.querySelectorAll(this.config.dropSpace)
    }

    printFiles(files){
        var output = [];
        for (var i = 0; i < files.length; i++) {
            let f = files[i]
            console.table({
                  name: f.name
                , type: f.type
                , size: f.size
                , lastModifiedDate : f.lastModifiedDate
            })
        }
    }
}


async function asyncMain() {
    const blob = new Blob([new Uint8Array(10 * 1024 * 1024)]); // any Blob, including a File
    const uploadProgress = document.getElementById("upload-progress");
    const downloadProgress = document.getElementById("download-progress");

    const xhr = new XMLHttpRequest();
    const success = await new Promise((resolve) => {
        xhr.upload.addEventListener("progress", (event) => {
            if (event.lengthComputable) {
                console.log("upload progress:", event.loaded / event.total);
                uploadProgress.value = event.loaded / event.total;
            }
        });
        xhr.addEventListener("progress", (event) => {
            if (event.lengthComputable) {
                console.log("download progress:", event.loaded / event.total);
                downloadProgress.value = event.loaded / event.total;
            }
        });

        xhr.addEventListener("loadend", () => {
            resolve(xhr.readyState === 4 && xhr.status === 200);
        });

        xhr.open("PUT", "https://httpbin.org/put", true);
        xhr.setRequestHeader("Content-Type", "application/octet-stream");
        xhr.send(blob);
    });
    console.log("success:", success);
}

// let runMain = function(){
//     asyncMain().catch(console.error);
// }

