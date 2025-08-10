
### Demo

{% spaceless %}
{% load link %}
<div class="demo-boxes">
    <div class="top layer">
        <div class="demo box">
            docs-1/
        </div>
        <div class="tool box">
            Optional Config
        </div>
        <div class="out box">
            docs/
        </div>
    </div>
    <div class="arrow layer">
        <div class="box"><div class="down arrow"></div></div>
        <div class="box"></div>
        <div class="box"><div class="up arrow"></div></div>
    </div>
    <div class="bottom layer">
        <div class="box">
            {% verbatim %}
                .md with {% tags %}
            {% endverbatim %}
        </div>
        <div class="box">
            Dev Tool
        </div>
        <div class="box">
            .md
        </div>
    </div>
</div>
<style type="text/css">
    .demo-boxes {
    /* border: solid; */
}

.demo-boxes .layer {
    /* border: solid; */
    display: flex;
    gap: 2rem;
    justify-content: center;
}

.layer .box {
    border: solid;
    width: 10rem;
    /* border-collapse: collapse; */
    height: 6rem;
    justify-content: center;
    display: flex;
    align-items: center;
    text-align: center;
    /* flex-grow: 1; */
    padding: 0;
    border-radius: 0.8em;
    margin: 0;
    white-space: normal;
}

.tool.box {
    color: #777;
    border-color: transparent;
}

.arrow.layer .box {
    border-color: transparent;
    height: auto;
    margin: 1em 0;
}

.bottom.layer .box {
}

.down.arrow, .up.arrow {
    border: solid;
    border-color: #3a5060;
    height: 3em;
    border-radius: 2em;
    position: relative;
    justify-content: center;
    display: flex;
}

.up.arrow:after, .down.arrow:after {
    content: ' ';
    border: solid 0.45em #324858;
    display: block;
    /* top: -0.5rem; */
    position: absolute;
    /* left: 0; */
    border-radius: 1em;
}

.down.arrow:after {bottom: -0.5em;}

.up.arrow:after {
    top: -0.5rem;
}
</style>
{% endspaceless %}
