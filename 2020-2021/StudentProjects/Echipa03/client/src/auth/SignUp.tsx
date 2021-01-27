import React, {useState} from "react";
import AuthService from "./AuthService";

const authService = AuthService();

const SignUp = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [errors, setError] = useState('');

    const onSignUp = async () => {
        try {
            const response = await authService.signUp(username, password);
            window.open("/SignIn", "_self");
        }
        catch (e) {
            setError(e.message);
        }
    };

    return (
        <div className={"container"}>
            <h1>Sign Up</h1>
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
            <button className="btn btn-primary w-100" onClick={onSignUp}>Sign Up</button>
            <div className={"text-danger text-center"}>{errors}</div>
        </div>
    );
};

export default SignUp;