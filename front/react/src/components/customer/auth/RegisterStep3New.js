import React from 'react';
import {
    Box,
    SimpleGrid,
    GridItem,
    chakra,
    Stack,
    FormControl,
    FormLabel,
    InputGroup,
    Input,
} from '@chakra-ui/react';

import Heading from "../../common/text/Heading";
import Text from "../../common/text/Text";
import Button from "../../common/buttons/Button";
import Autocomplete from "../../feature/Autocomplete";
import Countries from "./Countries";
const RegisterStep3Form = ({
                               street, setStreet, city, setCity, postalCode, setPostalCode,
                               country, setCountry, unitNo, setUnitNo, handlePrevious, handleNext
                           }) => {
    return (
        <Box
            bg="brand.600"
            _dark={{ bg: "#111" }}
            p={10}
        >
            <Box
                bg="brand.400"
                _dark={{ bg: "#111" }}
                p={30}
            >
                <SimpleGrid
                    display={{ base: "initial", md: "grid" }}
                    columns={{ md: 3 }}
                    spacing={{ md: 6 }}
                >
                    <GridItem colSpan={{ md: 1 }}>
                        <Box px={[4, 0]}>
                            <Heading color="brand.100" fontSize="5xl" fontWeight="md" lineHeight="10">
                                Register
                            </Heading>
                            <Text
                                mt={1}
                                fontSize="2xl"
                                color="gray.600"
                                _dark={{ color: "gray.400" }}
                            >
                                We're half way there.
                            </Text>
                        </Box>
                    </GridItem>
                    <GridItem mt={[5, null, 0]} colSpan={{ md: 2 }}>
                        <chakra.form
                            onSubmit={handleNext}
                            shadow="base"
                            rounded={[null, "md"]}
                            overflow={{ lg: "hidden" }}
                        >
                            <Stack
                                px={4}
                                py={8}
                                bg="white"
                                _dark={{ bg: "#141517" }}
                                spacing={6}
                                p={{ sm: 6 }}
                            >
                                <SimpleGrid columns={3} spacing={6}>
                                    <FormControl as={GridItem} colSpan={[3, 2]}>
                                        <FormLabel
                                            fontSize="md"
                                            fontWeight="md"
                                            color="gray.700"
                                            _dark={{ color: "gray.50" }}
                                        >
                                            City
                                        </FormLabel>

                                        <InputGroup size="sm">
                                            <Input
                                                type="text"
                                                value={city}
                                                placeholder="required"
                                                onChange={(e) => setCity(e.target.value)}
                                                focusBorderColor="brand.400"
                                                rounded="md"
                                                required
                                            />
                                        </InputGroup>
                                    </FormControl>

                                    <FormControl as={GridItem} colSpan={[3, 2]}>
                                        <FormLabel
                                            fontSize="md"
                                            fontWeight="md"
                                            color="gray.700"
                                            _dark={{ color: "gray.50" }}
                                        >
                                            Unit Number
                                        </FormLabel>

                                        <InputGroup size="sm">
                                            <Input
                                                type="text"
                                                value={unitNo}
                                                placeholder="required"
                                                onChange={(e) => setUnitNo(e.target.value)}
                                                focusBorderColor="brand.400"
                                                rounded="md"
                                                required
                                            />
                                        </InputGroup>
                                    </FormControl>

                                    <FormControl as={GridItem} colSpan={[3, 2]}>
                                        <FormLabel
                                            fontSize="md"
                                            fontWeight="md"
                                            color="gray.700"
                                            _dark={{ color: "gray.50" }}
                                        >
                                            Street
                                        </FormLabel>

                                        <InputGroup size="sm">
                                            <Input
                                                type="text"
                                                value={street}
                                                placeholder="required"
                                                onChange={(e) => setStreet(e.target.value)}
                                                focusBorderColor="brand.400"
                                                rounded="md"
                                                required
                                            />
                                        </InputGroup>
                                    </FormControl>

                                    <FormControl as={GridItem} colSpan={[3, 2]}>
                                        <FormLabel
                                            fontSize="md"
                                            fontWeight="md"
                                            color="gray.700"
                                            _dark={{ color: "gray.50" }}
                                        >
                                            Postal Code
                                        </FormLabel>

                                        <InputGroup size="sm">
                                            <Input
                                                type="text"
                                                value={postalCode}
                                                placeholder="Password"
                                                onChange={(e) => setPostalCode(e.target.value)}
                                                focusBorderColor="brand.400"
                                                rounded="md"
                                                required
                                            />
                                        </InputGroup>
                                    </FormControl>

                                    <FormControl as={GridItem} colSpan={[3, 2]}>
                                        <FormLabel fontSize="md" fontWeight="md" color="gray.700" _dark={{ color: "gray.50" }}>
                                            Country
                                        </FormLabel>
                                        <Autocomplete
                                            value={country}
                                            onChange={(e) => setCountry(e.target.value)}
                                            category={Countries}
                                        />
                                    </FormControl>
                                </SimpleGrid>
                            </Stack>
                            <Box
                                px={{ base: 4, sm: 6 }}
                                py={3}
                                bg="gray.50"
                                _dark={{ bg: "#121212" }}
                                textAlign="right"
                            >
                                <Button
                                    type="button"
                                    onClick={handlePrevious}
                                    colorScheme="brand"
                                    _focus={{ shadow: "" }}
                                    fontWeight="md"
                                >
                                    Back
                                </Button>
                                <Button
                                    type="submit"
                                    colorScheme="brand"
                                    _focus={{ shadow: "" }}
                                    fontWeight="md"
                                >
                                    Next
                                </Button>
                            </Box>
                        </chakra.form>
                    </GridItem>
                </SimpleGrid>
            </Box>
        </Box>
    );
};

export default RegisterStep3Form;