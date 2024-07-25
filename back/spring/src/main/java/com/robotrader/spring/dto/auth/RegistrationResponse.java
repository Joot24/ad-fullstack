package com.robotrader.spring.dto.auth;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;

@Setter
@Getter
@AllArgsConstructor
public class RegistrationResponse {
    private String message;
    private Long userId;
}