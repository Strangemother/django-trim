/* Plug and play toggle groups.

    Add a _click_ event to toggle a class on a target,
    For example a _button_ to show/hide a div.

Usage:

Include this JS Asset in your code:

    {% static "js/toggle-links.js" %}

Apply HTML assignments:

    <a data-target='foo-bar'>Click to toggle</a>

    <div data-name='foo-bar'>
        toggled content.
    </div>

add the JS.

    1. add "data-name" to a target
    2. add "data-target" to the clickable

The css class "toggle-show" "toggle-hidden" are switched per click.

    3. Optional add "data-group" to the clickable, for an _untoggle_ of
       all relatives.

Use CSS to Toggle the visibility of the panel:

    .toggle-hidden {
        display: none;
    }

    a.toggle-link {
        text-decoration: none;
    }

    a.toggle-link.toggle-selected {
        text-decoration: underline;
    }
 */

class ToggleHost {
    /* Host for the page. */
    targetSelector = "*[data-target]"
    activeSelector = "*[data-active]"
    preHidePanels = true

    enable() {
        /* Run on all items*/

        // Find all clickables - of which have not previously been activated
        let clickers = document.querySelectorAll(
            `${this.targetSelector}:not(${this.activeSelector})`
        )

        let preSelected = new Set()
        let host = this;

        clickers.forEach(function(n,i,a){
            // assign an onlick
            n.addEventListener('click', function(e){
                // Activate the change.
                host.onClick(n, e)
                // unclick the group.
                if(n.dataset.toggleGroup) {
                    host.deleselectGroup(n.dataset.toggleGroup, n)
                }
            })

            // Capture preflagged visible.
            if(n.classList.contains('toggle-selected')) {
                preSelected.add(n.dataset.target)
            }

            // prehide attached panels.
            host.getPanels(n).forEach((p) => {
                // Check for preselected class.
                if(p.classList.contains('toggle-show')) {
                    preSelected.add(p.dataset.target)
                }
                // hideit
                host.classToggleHide(p)
            })

            // activate
            n.dataset.active = true
        })

        // finally, enable the first active panel. This is default [0] or a *selected.
        console.log('Show', preSelected)
        for(let name of preSelected) {
            // higlight the clicker,
            // show the panel.
            let clickers = document.querySelectorAll(`*[data-target="${name}"]`)
            clickers.forEach(function(n){
                this.onClick(n)
                let toggleGroup = n.dataset.toggleGroup
                if(toggleGroup) {
                    this.deleselectGroup(toggleGroup, n)
                }

            }.bind(this))
        }
    }

    deleselectGroup(name, origin) {

        let host= this;
        // find all sibling by group
        let clickers = document.querySelectorAll(`*[data-toggle-group="${name}"]`)
        clickers.forEach(function(n,i,a){

            // Ignore the _current_
            if(n == origin) { return }

            n.classList.remove('toggle-selected')
            host.getPanels(n).forEach(host.classToggleHide)
        })
    }

    onClick(node, event) {
        let g = this.getGroup(node)
        let toggleFunc = this.classToggleShow
        let classFunc = 'add'

        if(g.length == 0) {
            // on/off
            let m = { 'true': true }
            let _switch = node.dataset.toggleOpen
            _switch = m[_switch]
            let r = !Boolean(_switch)

            // Add state for later.
            node.dataset.toggleOpen = r

            classFunc = r? 'add': 'remove'
            toggleFunc = r? this.classToggleShow: this.classToggleHide
        } else {
            // toggle on panel.
            console.log('Toggle switch')
            // node.classList.add('toggle-selected')
        }

        node.classList[classFunc]('toggle-selected')
        this.getPanels(node).forEach(toggleFunc)
    }

    getGroup(node) {
        // reurn all the matching grouped nodes.
        let name = this.getGroupName(node)
        let clickers = document.querySelectorAll(`*[data-toggle-group="${name}"]`)
        let res = [];
        clickers.forEach(function(n,i,a){
            // Ignore the _current_
            if(n == node) { return }
            res.push(n)
        })
        return res
    }

    getGroupName(node) {
        // return the group name of the node.
        return node.dataset.toggleGroup
    }

    classToggleHide(_n,i,a){
        // rehide the sibline clicker panels.
        _n.classList.remove('toggle-show')
        _n.classList.add('toggle-hidden')
    }

    classToggleShow(n,i,a){
        // Show panel.
        n.classList.add('toggle-show')
        n.classList.remove('toggle-hidden')
    }

    getPanels(node) {
        let targetName = node.dataset.target
        let panels = document.querySelectorAll(`*[data-name="${targetName}"]`)
        return panels
    }
}

window.toggleHost = new ToggleHost()
toggleHost.enable()