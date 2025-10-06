package org.heymouad.backend.dtos;


import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class ContractMessage {
    private String id;
    private String fileName;
    private String extractedText;
    private String header;
}
