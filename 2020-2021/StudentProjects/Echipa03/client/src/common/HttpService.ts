import Axios from "axios";
import CacheService from "./CacheService";

const SERVER_URL = "http://localhost:5000";

const HttpService = () => {
    const cacheService = CacheService();

    const get = (url: string): Promise<any> => {
        return Axios({
            "method": `GET`,
            "url": `${SERVER_URL}/${url}`,
            headers: createHeader(),
        }).then(response => {
            return response.data;
        });
    }

    const post = (url: string, body: any): Promise<any> => {
        console.log(createHeader());
        return Axios({
            "method": `POST`,
            "url": `${SERVER_URL}/${url}`,
            "data": body,
            headers: createHeader(),
        });
    }

    const createHeader = () => {
        const loggedUser = cacheService.getLoggedUser();

        if (loggedUser) {
            return {
                'Content-Type': 'application/json',
                'username': loggedUser,
            }
        }
        return {
            'Content-Type': 'application/json',
        }
    }

    return {
        SERVER_URL,
        get,
        post
    }
}

export default HttpService;