import React, {useState} from "react";
import AuthService from "./AuthService";

const authService = AuthService();

const SignIn = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [errors, setError] = useState('');

    const onSignIn = async () => {
        try {
            const response = await authService.signIn(username, password);
            window.open("/", "_self");
        }
        catch (e) {
            setError(e.message);
        }
    };

    return (
        <div className={"container"}>
            <h1>Sign In</h1>
            <div className="form-group">
                <label>Username</label>
                <input
                    value={username}
                    onChange={e => setUsername(e.target.value)}
                    className="form-control"
                />
            </div>
            <div className="form-group">
                <label>Password</label>
                <input
                    value={password}
                    onChange={e => setPassword(e.target.value)}
                    type="password"
                    className="form-control"
                />
            </div>
            <button className="btn btn-primary w-100" onClick={onSignIn}>Sign In</button>
            <div className={"text-danger text-center"}>{errors}</div>
        </div>
    );
};

export default SignIn;