import { useEffect, useState } from "react";

export function getLocalStorageValue(key, initialValue) {
    let savedValue;
    try {
        savedValue = JSON.parse(localStorage.getItem(key));
    } catch (e) {
        localStorage.removeItem(key);
    }
    if (savedValue) return savedValue;
    if (initialValue instanceof Function) return initialValue();
    return initialValue;
}

export default function useLocalStorage(key, initialValue) {
    const [value, setValue] = useState(() => getLocalStorageValue(key, initialValue))
    useEffect(() => {
        localStorage.setItem(key, JSON.stringify(value))
    }, [value])
    return [value, setValue]
}