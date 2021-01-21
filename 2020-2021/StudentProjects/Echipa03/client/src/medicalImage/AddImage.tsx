import React, {useState} from "react";
import useFileInput from "use-file-input";
import ImageService from "./ImageService";
import { saveAs } from 'file-saver';

const imageService = ImageService();

const AddImage = () => {
    const [statusMessage, setStatusMessage] = useState("");

    const handleFileSelect = useFileInput(
        async (files: FileList) => {
            setStatusMessage("Loading...");
            try {
                const response = await imageService.uploadImage(files);
                setStatusMessage("Downloading...");

                setTimeout(function () {
                    const fileName = response.data.filename;
                    downloadFile(fileName);
                    setStatusMessage("Done");
                }, 1000);
            }
            catch (e) {
                setStatusMessage("ERROR: " + e.message);
            }
        },
        {accept: ".dcm,.nii,image/*", multiple: true}
    );

    const downloadFile = (fileName: string) => {
        saveAs(imageService.getDownloadUrl(fileName), fileName);
    }

    return (
        <div className={"container"}>
            <p className={"display-4 text-center"}>Check for prostate cancer</p>
            <button onClick={handleFileSelect} className={"btn btn-primary w-100"}>
                Select the image(s) to analyze
            </button>
            <p className={"text-center text-success"}>{statusMessage}</p>
        </div>
    );
}

export default AddImage;