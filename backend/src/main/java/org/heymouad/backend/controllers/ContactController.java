package org.heymouad.backend.controllers;


import com.fasterxml.jackson.databind.ObjectMapper;
import jakarta.annotation.PostConstruct;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.heymouad.backend.dtos.ContractResponse;
import org.heymouad.backend.services.ContractService;
import org.heymouad.backend.services.servicesImpl.ContractReviewProducer;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.Map;
import java.util.Set;

@RequestMapping("/api/v1/")
@RestController
@RequiredArgsConstructor
@Slf4j
public class ContactController {
    private final ContractService contractService;
    private final ContractReviewProducer contractReviewProducer;
    private final RedisTemplate<String, String> redisTemplate;

    @PostMapping(value = "/contracts/review", consumes = "multipart/form-data")
    public ResponseEntity<Map<String, String>> reviewContract(@RequestParam("file") MultipartFile file) throws Exception
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

        return ResponseEntity.accepted().body(Map.of("id", id));
    }

    @GetMapping("/result/{id}")
    public ResponseEntity<?> getResult(@PathVariable String id) {
        String result = redisTemplate.opsForValue().get(id);
        log.warn(" [+] Result : {}", result);

        if (result == null) {
            return ResponseEntity.status(HttpStatus.ACCEPTED)
                    .body(Map.of("status", "processing", "message", "Result not ready yet."));
        }
        try {
            ObjectMapper mapper = new ObjectMapper();
            Map<String, Object> resultMap = mapper.readValue(result, Map.class);
            return ResponseEntity.ok(resultMap);
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(Map.of("status", "error", "message", "Result format error."));
        }
    }

    @PostConstruct
    public void logRedisConnection() {
        log.info("Redis connection factory: " + redisTemplate.getConnectionFactory().getConnection().toString());
    }

    @GetMapping("/debug/keys")
    public ResponseEntity<?> debugKeys() {
        Set<String> keys = redisTemplate.keys("*");
        return ResponseEntity.ok(keys);
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