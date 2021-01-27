import HttpService from "../common/HttpService";
import CacheService from "../common/CacheService";

const USER_API = "user";
const AUTH_API = "auth";
const httpService = HttpService();

const AuthService = () => {
    const cacheService = CacheService();

    const isLoggedIn = (): boolean => {
        let username = cacheService.getLoggedUser();
        return !!username;
    }

    const signUp = (username: string, password: string): Promise<boolean> => {
        const body = {
            username, password
        }
        return httpService.post(USER_API, body)
    }

    const signIn = (username: string, password: string): Promise<any> => {
        const body = {
            username, password
        }
        const response = httpService.post(AUTH_API, body);
        response.then(data => {
            cacheService.setLoggedUser(username);
        }, err => {
        });

        return response;
    }

    const signOut = () => {
        let aux = cacheService.getLoggedUser();
        cacheService.removeUser();
        console.log("Logged out. Bye, " + aux + "!");
    }

    const loggedUser = () => {
        return cacheService.getLoggedUser();
    }

    return {
        signUp,
        signIn,
        signOut,
        loggedUser,
        isLoggedIn
    }
}

export default AuthService;