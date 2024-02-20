import axios from "axios";
import validator from 'validator';


const USER = 'user'


interface SignupParams {
    email: string;
    password: string;
    nickname: string;
    gender: string;
    location: string;
}
export function signup(params: SignupParams) {
    return axios.post('/api/user/signup', params)
}

interface LoginParams {
    email: string;
    password: string;
}
export function login(params: LoginParams) {
    return axios.post('/api/user/login', params)
        .then(resp => {
            if (resp.data.access_token) {
                localStorage.setItem(USER, JSON.stringify(resp.data));
            }
            return resp.data
        });
}

export function logout() {
    localStorage.removeItem(USER)
}

export default {
    signup,
    login,
    logout,
}