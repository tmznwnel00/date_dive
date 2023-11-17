import { useState } from 'react';
import axios from 'axios';

function Login() {
    const [email, setEmail] = useState('email');
    const [password, setPassword] = useState('password');

    const onChange1 = (e) => {
        setEmail(e.target.value);
    };
    const onChange2 = (e) => {
        setPassword(e.target.value);
    };
    async function handleSubmit() {
        try{
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
                <input onChange={onChange1} value={email}/>
            </div>
            <div>
                <input onChange={onChange2} value={password}/>
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