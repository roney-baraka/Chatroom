import React, {useState} from 'react';
import{View, Text, TextInput, Button,Alert} from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';

const LoginScreen = ({ navigattion }) => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = userState('');

    const login = async () =>{
        //Replace the flask server Url
        const response = await fetch ('http://your-server-ip:5000/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'appliction/json'
            },
            body: JSON.stringify({username, password}),
        });

        const data = await response.json();
    }


};