import React, {useState} from "react";
import useFileInput from "use-file-input";
import ImageService from "./ImageService";
import { saveAs } from 'file-saver';
import { NavItem } from "react-bootstrap";

const imageService = ImageService();

const SendImageToServer = () => {
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
            <NavItem onClick={handleFileSelect} className={"btn"}>
                Prostate cancer detection
            </NavItem>   

    );
}

export default SendImageToServer;