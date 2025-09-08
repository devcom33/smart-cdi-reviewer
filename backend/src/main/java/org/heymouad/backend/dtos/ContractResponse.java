package org.heymouad.backend.dtos;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.List;

@JsonInclude(JsonInclude.Include.NON_EMPTY)
public record ContractResponse(
        @JsonProperty("file_name") String filename,
        @JsonProperty("extracted_text") String extractedText,
        @JsonProperty("header") String header,
        @JsonProperty("clauses") List<ClauseResponse> clauses
) {}
