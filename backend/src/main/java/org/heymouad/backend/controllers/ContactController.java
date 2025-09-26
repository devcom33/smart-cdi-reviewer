package org.heymouad.backend.controllers;


import lombok.RequiredArgsConstructor;
import org.heymouad.backend.dtos.ContractResponse;
import org.heymouad.backend.services.ContractReviewConsumerService;
import org.heymouad.backend.services.ContractService;
import org.heymouad.backend.services.servicesImpl.ContractReviewProducer;
import org.springframework.data.redis.core.RedisTemplate;
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
    private final ContractService contractService;
    private final ContractReviewProducer contractReviewProducer;
    private final RedisTemplate<String, String> redisTemplate;

    @PostMapping(value = "/contracts/review", consumes = "multipart/form-data")
    public ResponseEntity<String> reviewContract(@RequestParam("file") MultipartFile file) throws Exception
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

        ContractResponse contractResponse = contractService.processContract(file);

        String id = contractReviewProducer.sendToQueue(contractResponse);

        return ResponseEntity.accepted().body("Contract uploaded. ID = " + id);
    }

    @GetMapping("/result/{id}")
    public ResponseEntity<String> getResult(@PathVariable String id) {
        String result = redisTemplate.opsForValue().get(id);
        if (result == null) {
            return ResponseEntity.status(HttpStatus.PROCESSING)
                    .body("Result not ready yet.");
        }
        return ResponseEntity.ok(result);
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