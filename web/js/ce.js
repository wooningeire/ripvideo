import {ce} from "./util.js";

const InputTime = (() => {
    class InputTime extends HTMLElement {
        constructor() {
            super();

            this.attachShadow({mode: "open"});

            const stylesheet = ce("link");
            stylesheet.href = "./css/input-time.css";
            stylesheet.rel = "stylesheet";
            this.shadowRoot.appendChild(stylesheet);

            const content = ce("span");
            content.classList.add("content");

            const newInput = () => {
                const input = ce("input");
                input.type = "text";

                input.addEventListener("input", () => {
                    this.dispatchEvent(new CustomEvent("input"));
                });

                return input;
            };

            const newSeparator = () => {
                const span = ce("span");
                span.textContent = ":";
                span.classList.add("separator");
                return span;
            };

            this.inputs = {
                hours: newInput(),
                minutes: newInput(),
                seconds: newInput(),
            };
            this.oldValues = {};

            for (let key of Object.keys(this.inputs)) {
                this[key] = 0;

                this.inputs[key].addEventListener("input", event => {
                    this[key] = event.currentTarget.value;
                });
            }

            const endInput = key => {
                const input = this.inputs[key];
                const inputLength = input.value.length;
                input.focus();
                input.setSelectionRange(inputLength, inputLength);
            };

            const homeInput = key => {
                const input = this.inputs[key];
                input.focus();
                input.setSelectionRange(0, 0);
            };

            const ifApplicableMoveLeftFrom = (key, event) => {
                const input = this.inputs[key];

                const selectionLength = input.selectionEnd - input.selectionStart;
                if (event.key === "ArrowLeft" && input.selectionStart === 0 && selectionLength === 0) {
                    event.preventDefault();
                    endInput(InputTime.keyOrder[InputTime.keyOrder.indexOf(key) - 1]);
                }
            };

            const ifApplicableMoveRightFrom = (key, event) => {
                const input = this.inputs[key];

                const selectionLength = input.selectionEnd - input.selectionStart;
                if (event.key === "ArrowRight" && input.selectionEnd === input.value.length && selectionLength === 0) {
                    event.preventDefault();
                    homeInput(InputTime.keyOrder[InputTime.keyOrder.indexOf(key) + 1]);
                }
            };

            this.inputs.hours.addEventListener("keydown", event => {
                ifApplicableMoveRightFrom("hours", event);
            });

            this.inputs.minutes.addEventListener("keydown", event => {
                ifApplicableMoveLeftFrom("minutes", event);
                ifApplicableMoveRightFrom("minutes", event);
            });

            this.inputs.seconds.addEventListener("keydown", event => {
                ifApplicableMoveLeftFrom("seconds", event);
            });

            content.appendChild(this.inputs.hours);
            content.appendChild(newSeparator());
            content.appendChild(this.inputs.minutes);
            content.appendChild(newSeparator());
            content.appendChild(this.inputs.seconds);

            this.shadowRoot.appendChild(content);
        }

        get value() {
            return `${pad(this.hours)}:${pad(this.minutes)}:${pad(this.seconds)}`;
        }
        set value(value) {
            const parameters = value.toString().split(":").reverse().map(numerifyString);
            
            this.seconds = parameters[0] || 0;
            this.minutes = parameters[1] || 0;
            this.hours = parameters[2] + (parameters[3] || 0) * 24 || 0;
        }

        get seconds() {
            return this.oldValues.seconds;
        }
        set seconds(value) {
            setSingleParameter("seconds", value, this);
        }

        get minutes() {
            return this.oldValues.minutes;
        }
        set minutes(value) {
            setSingleParameter("minutes", value, this);
        }

        get hours() {
            return this.oldValues.hours;
        }
        set hours(value) {
            setSingleParameter("hours", value, this);
        }
    }
    Object.defineProperty(InputTime, "keyOrder", {
        value: ["hours", "minutes", "seconds"],
    });

    function numerifyString(string, doTrim=true) {
        string = string.toString().replace(/[^0-9]/g, "");
        return Number(doTrim ? string.substring(string.length - 2, string.length) : string);
    }

    function pad(n) {
        return n.toString().padStart(2, "0");
    }

    function setSingleParameter(key, value, inputTime) {
        const input = inputTime.inputs[key];
        const setHours = key !== "hours";

        if (typeof value === "string") {
            value = numerifyString(value, setHours);
        }

        const caretPosition = input.value.length - input.selectionEnd;

        let newValue = value;

        if (isNaN(value)) {
            newValue = inputTime.oldValues[key];
        } else if (setHours && value >= 60) {
            newValue = 59;
        } else if (value < 0) {
            newValue = 0;
        }

        inputTime.oldValues[key] = newValue;
        input.value = pad(newValue);
        resizeInput(input);

        // uses a new `input.value` value
        const caretPositionSet = input.value.length - caretPosition;
        input.setSelectionRange(caretPositionSet, caretPositionSet);
    }

    function measureTextWidth(text) {
        const context = ce("canvas").getContext("2d");
        context.font = getComputedStyle(document.body).font;
        return context.measureText(text).width;
    }

    function resizeInput(input) {
        input.style.width = `${measureTextWidth(input.value)}px`;
    }

    return InputTime;
})();
customElements.define("input-time", InputTime);