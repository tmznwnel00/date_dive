import validator from 'validator';
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { login, ACCESS_TOKEN } from './AuthService.ts';
import { useForm } from 'react-hook-form';
import { Button, FormControl, InputLabel, MenuItem, Select, TextField, FormLabel, RadioGroup, Radio, FormControlLabel, FormHelperText } from '@mui/material';
import { getLocalStorageValue } from '../../hooks/useStorageHook'
import useCurrentUser from '../../hooks/useUserHook.js';


function Login() {
    const navigate = useNavigate();
    const { register, handleSubmit, formState: { errors }} = useForm();

    // Redirect to the home page when auth token is set
    const user = useCurrentUser()
    useEffect(() => {
        if (user) {
            navigate('/')
        }
    }, [user])

    return (
        <form onSubmit={handleSubmit(async (data) => {
            await login(data)
                .then(() => {
                    navigate('/')
                })
                .catch(e => {
                    alert('Login Failed');
                    console.error(e);
                })
        })}>
            <FormControl fullWidth margin="normal">
                <TextField
                    {...register('email', {
                        required: true,
                        validate: (value) => {
                            if (!validator.isEmail(value)) {
                                return 'Email address is not valid';
                            }
                        }
                    })}
                    label="Email"
                    variant="outlined"
                    placeholder='abc@datedive.com'
                    error={!!errors.email}
                    helperText={errors.email?.message}
                />
            </FormControl>
            <FormControl fullWidth margin="normal">
                <TextField
                    {...register('password', {
                        required: true,
                    })}
                    label="Password"
                    type='password'
                    variant="outlined"
                    placeholder='******'
                    error={!!errors.password}
                    helperText={errors.password?.message}
                />
            </FormControl>
            <Button type='submit'>
                login
            </Button>
        </form>
    )
}

export default Login;