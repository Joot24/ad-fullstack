import { useState, useEffect } from 'react';
import customerService from '../services/CustomerService';

const useCustomer = () => {
    const [customer, setCustomer] = useState(null);

    const getCustomer = async () => {
        try {
            const response = await customerService.getCustomer();
            console.log('Fetched customer data:', response.data); // 调试日志
            setCustomer(response.data);
        } catch (error) {
            console.error('Error fetching customer data', error);
        }
    };

    useEffect(() => {
        getCustomer();
    }, []);

    return { customer, getCustomer };
};

export default useCustomer;