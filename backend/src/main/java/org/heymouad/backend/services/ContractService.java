package org.heymouad.backend.services;

import org.apache.tika.exception.TikaException;
import org.heymouad.backend.dtos.ContractResponse;
import org.springframework.web.multipart.MultipartFile;
import org.xml.sax.SAXException;

import java.io.IOException;

public interface ContractService {
    ContractResponse processContract(MultipartFile file) throws IOException, TikaException, SAXException;
}
