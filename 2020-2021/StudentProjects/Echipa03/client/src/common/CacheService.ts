const CacheService = () => {
    const getLoggedUser  = (): string | null=> {
        return localStorage.getItem("username");
    }

    const setLoggedUser  = (username : string): string | null => {
        localStorage.setItem("username", username);
        return username;
    }

    const removeUser  = () => {
        return localStorage.removeItem("username");
    }

    return {
        getLoggedUser,
        setLoggedUser,
        removeUser,
    }
}

export default CacheService;