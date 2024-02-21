import axios from "axios";
import validator from 'validator';


export const ACCESS_TOKEN = 'access_token'
axios.interceptors.request.use(function (config) {
    config.headers.Authorization = `bearer ${localStorage.getItem(ACCESS_TOKEN)}`;
    return config;
});

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
                localStorage.setItem(ACCESS_TOKEN, resp.data.access_token);
            }
            return resp.data
        });
}


export function logout() {
    localStorage.removeItem(ACCESS_TOKEN)
}

export default {
    signup,
    login,
    logout,
    ACCESS_TOKEN,
}