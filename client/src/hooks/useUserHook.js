import { useState, useEffect } from "react"
import { ACCESS_TOKEN } from "../pages/user/AuthService.ts";

import useLocalStorage from "./useStorageHook"
import axios from "axios";


let current_user;
let current_user_token;

export default function useCurrentUser() {
    const [user, setUser] = useState();
    const [token, setToken] = useLocalStorage(ACCESS_TOKEN);
    useEffect(() => {
        if (token !== current_user_token) {
            axios.get("/api/user/myinfo").then((resp) => {
                current_user = resp.data;
                current_user_token = token
                setUser(current_user)
            }).catch(() => {
                current_user = null
                current_user_token = null;
                setToken()
            })
        }
    }, [token])
    return current_user;
}