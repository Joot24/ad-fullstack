import React from 'react';
import FourQuantLogo from "../../../assets/images/fourquant-logo.png"

import { Box, Stack, Flex, Image, HStack, Link, Divider, VStack, Icon, Text } from '@chakra-ui/react';
import { FaFacebookF, FaLinkedinIn } from 'react-icons/fa';
import { FiTwitter } from 'react-icons/fi';
import { GrInstagram } from 'react-icons/gr';


const Footer = () => {
    return (
        <Box
            bg="white"
            _dark={{
                bg: "gray.600",
            }}
        >
            <Stack
                direction={{
                    base: "column",
                    lg: "row",
                }}
                w="full"
                justify="space-between"
                p={10}
            >
                <Flex justify="center">
                    <Image
                        src={FourQuantLogo}
                        alt="Company Logo"
                        width={{
                            base: "200px",
                            lg: "300px",
                        }}
                        height={{
                            base: "70px",
                            lg: "100px",
                        }}
                        my={{
                            base: 2,
                            lg: 0,
                        }}
                    />
                </Flex>
                <HStack
                    alignItems="start"
                    flex={1}
                    justify="space-around"
                    fontSize={{
                        base: "12px",
                        md: "16px",
                    }}
                    color="gray.800"
                    _dark={{
                        color: "white",
                    }}
                    textAlign={{
                        base: "center",
                        md: "left",
                    }}
                >
                    <Flex justify="start" direction="column">
                        <Link textTransform="uppercase">Support</Link>
                        <Link textTransform="uppercase">Resources</Link>
                    </Flex>
                    <Flex justify="start" direction="column">
                        <Link textTransform="uppercase">Services</Link>
                        <Link textTransform="uppercase">MarketPlace and Fees</Link>
                    </Flex>
                </HStack>
                <HStack
                    alignItems="start"
                    flex={1}
                    justify="space-around"
                    fontSize={{
                        base: "12px",
                        md: "16px",
                    }}
                    color="gray.800"
                    _dark={{
                        color: "white",
                    }}
                    textAlign={{
                        base: "center",
                        md: "left",
                    }}
                >
                    <Flex justify="start" direction="column">
                        <Link textTransform="uppercase">Show Case</Link>
                        <Link textTransform="uppercase">Security</Link>
                        <Link textTransform="uppercase">Trust and Safety</Link>
                    </Flex>
                    <Flex justify="start" direction="column">
                        <Link textTransform="uppercase">About Us</Link>
                        <Link textTransform="uppercase">Contact Us</Link>

                    </Flex>
                </HStack>
            </Stack>
            <Divider
                w="95%"
                mx="auto"
                color="gray.600"
                _dark={{
                    color: "#F9FAFB",
                }}
                h="3.5px"
            />
            <VStack py={3}>
                <HStack justify="center">
                    <Link>
                        <Icon
                            color="gray.800"
                            _dark={{
                                color: "white",
                            }}
                            h="20px"
                            w="20px"
                            as={FaFacebookF}
                        />
                    </Link>
                    <Link>
                        <Icon
                            color="gray.800"
                            _dark={{
                                color: "white",
                            }}
                            h="20px"
                            w="20px"
                            as={FiTwitter}
                        />
                    </Link>
                    <Link>
                        <Icon
                            _dark={{
                                color: "white",
                            }}
                            h="20px"
                            w="20px"
                            as={GrInstagram}
                        />
                    </Link>
                    <Link>
                        <Icon
                            _dark={{
                                color: "white",
                            }}
                            h="20px"
                            w="20px"
                            as={FaLinkedinIn}
                        />
                    </Link>
                </HStack>

                <Text
                    textAlign="center"
                    fontSize="smaller"
                    _dark={{
                        color: "white",
                    }}
                >
                    &copy;Copyright. All rights reserved.
                </Text>
            </VStack>
        </Box>
    );
};

export default Footer;
