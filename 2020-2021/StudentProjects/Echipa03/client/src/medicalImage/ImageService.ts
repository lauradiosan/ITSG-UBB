import HttpService from "../common/HttpService";
import CacheService from "../common/CacheService";

const IMAGE_API = "images";
const httpService = HttpService();

const ImageService = () => {
    const cacheService = CacheService();

    const uploadImage = (images: FileList): Promise<any> => {
        const formData = new FormData();
        for (let i = 0; i < images.length; i++) {
            formData.append(images[i].name, images[i]);
        }
        return httpService.post(IMAGE_API, formData);
    }

    const getDownloadUrl = (fileName: string): string => {
        return httpService.SERVER_URL + "/analyzed_images/" + fileName;
    }

    const getDownloadUrlForUser = (fileName: string): string => {
        const username = cacheService.getLoggedUser();
        return getDownloadUrl(fileName) + "?username=" + username;
    }

    const getUserFolders = (): Promise<any> => {
        const username = cacheService.getLoggedUser();
        return httpService.get("my_images");
    }

    return {
        uploadImage,
        getDownloadUrl,
        getUserFolders,
        getDownloadUrlForUser,
    }
}

export default ImageService;