import { useState } from 'react';
import axios from 'axios';

function Login() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const onChange1 = (e) => {
        setEmail(e.target.value);
    };
    const onChange2 = (e) => {
        const inputPassword = e.target.value;
        const maskedPassword = inputPassword.replace(/./g, '*');
        setPassword(maskedPassword);
    };
    async function handleSubmit() {
        try {
            const response = await axios.post('/api/user/login', {
                email: email,
                password: password
            }
            )
        } catch (error) {
            console.log(error);
        }
    };

    return (
        <div>
            <div>
                email: <input onChange={onChange1} value={email} placeholder="Email" />
            </div>
            <div>
                password: <input onChange={onChange2} value={password} placeholder="Password" />
            </div>
            <div>
                <button onClick={handleSubmit}>
                    login
                </button>
            </div>
        </div>
    )
}

export default Login;