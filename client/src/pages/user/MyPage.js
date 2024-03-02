import validator from 'validator';
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { login, ACCESS_TOKEN } from './AuthService.ts';
import { useForm } from 'react-hook-form';
import { Button, FormControl, InputLabel, MenuItem, Select, TextField, FormLabel, RadioGroup, Radio, FormControlLabel, FormHelperText } from '@mui/material';
import useCurrentUser from '../../hooks/useUserHook.js';


function MyPage() {
    const navigate = useNavigate();
    const user = useCurrentUser();

    return <>
        <div>{JSON.stringify(user)}</div>
        <Button onClick={() => navigate('/')}>Home</Button>
    </>
}

export default MyPage;