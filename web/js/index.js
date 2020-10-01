import {qs, ce} from "./util.js";
import "./ce.js";

const shared = {
    videoDataBase64: "",
    
    get doExtractVisual() {
        return qs("input.do-visual").checked;
    },
    get doExtractAudio() {
        return qs("input.do-audio").checked;
    },

    get speedFactor() {
        const speedFactor = parseInt(qs("input.speed").value);
        return isNaN(speedFactor) ? 1 : speedFactor;
    },
};

const video = ce("video");
video.addEventListener("load", () => {

});

const videoInput = qs(".video-input");
videoInput.addEventListener("input", () => {
    const file = videoInput.files[0];
    
    if (!file || file.type.substring(0, file.type.indexOf("/")) !== "video") {
        shared.videoDataBase64 = "";
        //video.src = "";
        return;
    }

    const reader = new FileReader();

    reader.onload = () => {
        shared.videoDataBase64 = reader.result.substring(reader.result.indexOf(",") + 1);
        //video.src = reader.result;
        oninput();
    };

    reader.readAsDataURL(file);
});

function oninput() {
    console.log("form input");
    button.disabled = Boolean(
        !shared.videoDataBase64 ||
        !(qs("input.do-visual").checked || qs("input.do-audio").checked)
    );
}

qs("form > div").addEventListener("input", oninput);

const button = qs("button.extract");
qs("form").addEventListener("submit", async event => {
    console.log(`[JS] Sending video data (${shared.videoDataBase64.length} bytes base64)`);
    setStatus(`Sending video data (${shared.videoDataBase64.length} bytes base64)`);

    event.preventDefault();

    // video_data: str, 
    // shared.videoDataBase64,
    button.disabled = true;
    await eel.extract(shared.videoDataBase64, shared.doExtractVisual, shared.doExtractAudio, shared.speedFactor)();
    button.disabled = false;

    setStatus("Done");
});

eel.expose(polo);
function polo() {
    setStatus("Video data received. Now processing video data");
}

function setStatus(text) {
    qs("p.status").textContent = text;
}