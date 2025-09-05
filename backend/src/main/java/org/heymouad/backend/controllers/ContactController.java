package org.heymouad.backend.controllers;


import lombok.RequiredArgsConstructor;
import org.heymouad.backend.dtos.ContractResponse;
import org.heymouad.backend.services.ClauseExtractionService;
import org.heymouad.backend.services.ContractService;
import org.heymouad.backend.services.FilesStorageService;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.Set;

@RequestMapping("/api/v1/")
@RestController
@RequiredArgsConstructor
public class ContactController {
    private final FilesStorageService filesStorageService;
    private final ContractService contractService;

    @PostMapping(value = "/contracts/upload", consumes = "multipart/form-data")
    public ResponseEntity<ContractResponse> uploadContract(@RequestParam("file") MultipartFile file) throws Exception
    {
        Set<String> allowedTypes = Set.of(
                "application/pdf",
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        );

        if (file.getSize() > 5 * 1024 * 1024)
        {
            throw new IOException("File Too Large");
        }

        String fileType = file.getContentType();

        if (fileType == null || (!allowedTypes.contains(fileType)))
            throw new IllegalArgumentException("Unsupported file type: " + fileType);

        return ResponseEntity.ok(contractService.processContract(file));
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