import validator from 'validator';
import { useNavigate } from 'react-router-dom';
import { koreaLocation } from '../../constants/constants';
import { signup } from './AuthService.ts';
import { Controller, useForm } from 'react-hook-form';
import { Button, FormControl, InputLabel, MenuItem, Select, TextField, FormLabel, RadioGroup, Radio, FormControlLabel, FormHelperText } from '@mui/material';

function Signup() {
    const navigate = useNavigate();
    const { control, register, handleSubmit, watch, formState: { errors } } = useForm();
    const mainlocation = watch('mainlocation');

    return (
        <form onSubmit={handleSubmit(async (data) => {
            await signup({ ...data, location: data.mainlocation + ' ' + data.sublocation })
                .then(() => navigate('/login'))
                .catch((e) => {
                    alert(`Signup failed: ${e.response?.data?.detail || e.message}`);
                    console.error(e);
                });
        })}>
            <FormControl fullWidth margin="normal">
                <TextField
                    {...register('email', {
                        required: 'Email is required',
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
                        required: 'Password is required',
                        validate: (value) => {
                            if (!validator.isStrongPassword(value, {
                                minLength: 8,
                                minNumbers: 1
                            })) {
                                return "Password must be longer than 8 characters and include at least one number";
                            }
                        }
                })}
                    label="Password"
                    type='password'
                    variant="outlined"
                    placeholder='******'
                    error={!!errors.password}
                    helperText={errors.password?.message}
                />
            </FormControl>
            <FormControl fullWidth margin="normal">
                <TextField
                    {...register('nickname', { required: 'Nickname is required' })}
                    label="Nickname"
                    variant="outlined"
                    error={!!errors.nickname}
                    helperText={errors.nickname?.message}
                />
            </FormControl>
            <FormControl fullWidth margin="normal" error={!!errors.gender}>
                <FormLabel component="legend">Gender</FormLabel>
                <Controller
                    name="gender"
                    control={control}
                    rules={{
                        required: 'Select your gender'
                    }}
                    defaultValue=''
                    render={({ field }) => {
                        return <RadioGroup {...field}>
                            <FormControlLabel value="male" control={<Radio />} label="Male" />
                            <FormControlLabel value="female" control={<Radio />} label="Female" />
                        </RadioGroup>
                    }} />
                <FormHelperText>{errors.gender?.message}</FormHelperText>
            </FormControl>
            <FormControl fullWidth margin="normal" error={!!errors.mainlocation}>
                <InputLabel>시/도</InputLabel>
                <Controller
                    name="mainlocation"
                    rules={{
                        required: 'Select your primary location'
                    }}
                    control={control}
                    defaultValue=''
                    render={({ field }) => {
                        return <Select {...field}>
                            {Object.keys(koreaLocation).map((division) => (
                                <MenuItem key={division} value={division}>
                                    {division}
                                </MenuItem>
                            ))}
                        </Select>
                    }} />
                <FormHelperText>{errors.mainlocation?.message}</FormHelperText>
            </FormControl>
            <FormControl fullWidth margin="normal">
                <InputLabel>시/구/군</InputLabel>
                <Select
                    {...register('sublocation')}
                    label="Sub-location"
                    defaultValue={''}
                >
                    {koreaLocation[mainlocation]?.map((subDivision) => (
                        <MenuItem key={subDivision} value={subDivision}>
                            {subDivision}
                        </MenuItem>
                    ))}
                </Select>
            </FormControl>
            <Button type='submit' variant="contained">
                Signup
            </Button>
        </form>
    );
}

export default Signup;
