import React from 'react';
import Button from './Button';

const ButtonBlack = ({ variant, size, type, colorScheme, onClick, href, children, ...props }) => {
    return (
        <Button
            size={size}
            variant={variant}
            colorScheme={colorScheme}
            href={href}
            onClick={onClick}
            bg="black"
            color="white"
            _hover={{ bg: 'gray.700' }}
            _active={{ bg: 'gray.800' }}
            {...props}
        >
            {children}
        </Button>
    );
};

export default ButtonBlack;
