import React, {useEffect, useState} from 'react';
import ImageService from "../medicalImage/ImageService";

const ImagesList = () => {
    const imageService = ImageService();
    const [folderNames, setFolderNames] = useState([]);

    useEffect(() => {
        imageService.getUserFolders().then(response => {
            setFolderNames(response.folders);
        });
    }, [])

    const download = (folderName: string) => {
        saveAs(imageService.getDownloadUrlForUser(folderName), folderName);
    }

    return (
        <div className={"container"}>{folderNames.map((folderName, index) => (
            <div key={index} className="card col-4">
                <div className="card-body">
                    <label className={'m-1'}>{folderName}</label>
                    <button className="btn btn-primary m-1 float-right" onClick={() => download(folderName)}>Download</button>
                </div>
            </div>
            ))}
        </div>
    );
}

export default ImagesList;