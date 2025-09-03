package org.heymouad.backend.controllers;


import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;

@RequestMapping("/api/v1/")
public class ContactController {

    @PostMapping("/contracts/upload")
    public ResponseEntity<?> uploadContract()
    {
        return null;
    }

    @GetMapping("/contracts")
    public ResponseEntity<?> getAllContracts()
    {
        return null;
    }

    @GetMapping("/contracts/{id}")
    public ResponseEntity<?> getContractById(@PathVariable Long id)
    {
        return null;
    }
}