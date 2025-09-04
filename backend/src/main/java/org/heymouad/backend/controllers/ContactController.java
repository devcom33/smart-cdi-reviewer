package org.heymouad.backend.controllers;


import lombok.RequiredArgsConstructor;
import org.heymouad.backend.services.FilesStorageService;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

@RequestMapping("/api/v1/")
@RestController
@RequiredArgsConstructor
public class ContactController {
    private final FilesStorageService filesStorageService;

    @PostMapping(value = "/contracts/upload", consumes = "multipart/form-data")
    public ResponseEntity<String> uploadContract(@RequestParam("file") MultipartFile file)
    {
        String message;
        try {
            filesStorageService.saveFile(file);
            message = "Uploaded the file successfully: " + file.getOriginalFilename();
            return new ResponseEntity<>(message, HttpStatus.OK);
        } catch (Exception e) {
            message = "Could not upload the file: " + file.getOriginalFilename() + ". Error: " + e.getMessage();
            return new ResponseEntity<>(message, HttpStatus.EXPECTATION_FAILED);
        }
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