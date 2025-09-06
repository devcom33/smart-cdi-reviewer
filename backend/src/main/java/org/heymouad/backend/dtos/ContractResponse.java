package org.heymouad.backend.dtos;

import java.util.List;

public record ContractResponse(String filename, String extractedText, List<String> clauses) {
}
