class DocumentGeneratorApp {
    constructor() {
        this.currentRequirement = '';
        this.currentAnswers = {};
        this.currentDocument = null;
        this.coverageData = null;
        this.documentType = 'user-story'; // default
        this.sectionImages = {}; // Store images per section
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        // Corporate Tiles Selection
        this.initializeCorporateTiles();
        
        // Step navigation
        document.getElementById('analyze-btn').addEventListener('click', () => this.analyzeRequirement());
        document.getElementById('generate-btn').addEventListener('click', () => this.generateDocument());
        document.getElementById('generate-from-qa').addEventListener('click', () => this.generateDocument());
        document.getElementById('back-to-requirement').addEventListener('click', () => this.showStep('requirement'));
        document.getElementById('back-to-coverage').addEventListener('click', () => this.showStep('coverage'));
        document.getElementById('back-to-qa').addEventListener('click', () => this.showStep('coverage'));
        document.getElementById('start-over').addEventListener('click', () => this.startOver());

        // Export buttons
        document.getElementById('export-word').addEventListener('click', () => this.exportDocument('word'));
        document.getElementById('export-pdf').addEventListener('click', () => this.exportDocument('pdf'));

        // Modal close
        document.querySelector('.close').addEventListener('click', () => this.hideError());
        
        // Enter key handling
        document.getElementById('requirement-input').addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && e.ctrlKey) {
                this.analyzeRequirement();
            }
        });
    }

    initializeCorporateTiles() {
        const tiles = document.querySelectorAll('.document-tile');
        const hiddenInput = document.getElementById('selected-document-type');
        
        tiles.forEach(tile => {
            // Click handler for tile selection
            tile.addEventListener('click', () => {
                // Remove selected class from all tiles
                tiles.forEach(t => t.classList.remove('selected'));
                
                // Add selecting animation
                tile.classList.add('selecting');
                setTimeout(() => tile.classList.remove('selecting'), 300);
                
                // Add selected class to clicked tile
                tile.classList.add('selected');
                
                // Update document type
                const docType = tile.dataset.type;
                this.documentType = docType;
                hiddenInput.value = docType;
                
                // Update UI
                this.updateUIForDocumentType();
                
                // Update button text
                this.updateAnalyzeButton(docType);
            });
            
            // Keyboard navigation
            tile.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    tile.click();
                }
            });
            
            // Make tiles focusable
            tile.setAttribute('tabindex', '0');
        });
        
        // Set default selection
        const defaultTile = document.querySelector('.document-tile[data-type="user-story"]');
        if (defaultTile) {
            defaultTile.classList.add('selected');
            this.updateAnalyzeButton('user-story');
        }
    }
    
    updateAnalyzeButton(docType) {
        const analyzeBtn = document.getElementById('analyze-btn');
        const docTypeNames = {
            'user-story': 'User Story',
            'brd': 'Business Requirements',
            'frd': 'Functional Requirements',
            'srd': 'System Architecture',
            'cr': 'Change Request'
        };
        
        analyzeBtn.textContent = `Analyze for ${docTypeNames[docType]}`;
    }

    updateUIForDocumentType() {
        const titleElement = document.getElementById('generated-document-title');
        
        // Update title based on document type
        if (titleElement) {
            const titles = {
                'user-story': 'Step 4: Generated Enterprise User Story',
                'brd': 'Step 4: Generated Business Requirements Document',
                'frd': 'Step 4: Generated Functional Requirements Document',
                'srd': 'Step 4: Generated System Requirements Document'
            };
            titleElement.textContent = titles[this.documentType] || 'Step 4: Generated Document';
        }
    }

    showStep(step) {
        // Hide all sections
        document.querySelectorAll('.step-section').forEach(section => {
            section.classList.remove('active');
        });

        // Show target section
        document.getElementById(`${step}-section`).classList.add('active');
    }

    showLoading(message = 'Processing...') {
        document.getElementById('loading-text').textContent = message;
        document.getElementById('loading-overlay').classList.add('show');
    }

    hideLoading() {
        document.getElementById('loading-overlay').classList.remove('show');
    }

    showError(message) {
        document.getElementById('error-message').textContent = message;
        document.getElementById('error-modal').style.display = 'block';
    }

    hideError() {
        document.getElementById('error-modal').style.display = 'none';
    }

    async analyzeRequirement() {
        const requirement = document.getElementById('requirement-input').value.trim();
        
        if (!requirement) {
            this.showError('Please enter a requirement description.');
            return;
        }

        this.currentRequirement = requirement;
        this.showLoading('Analyzing requirement...');

        try {
            
            // Choose endpoint based on document type
            const endpoint = this.documentType === 'brd' ? '/analyze_brd' : 
                           this.documentType === 'frd' ? '/analyze_frd' : 
                           this.documentType === 'srd' ? '/analyze_srd' : '/analyze';
            
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    requirement
                })
            });

            const data = await response.json();
            
            // Debug logging
            console.log('Analysis Response:', data);
            console.log('Coverage Analysis:', data.coverage_analysis);

            if (!response.ok) {
                throw new Error(data.error || 'Analysis failed');
            }

            this.coverageData = data.coverage_analysis;
            this.renderCoverageAnalysis(data.coverage_analysis);
            this.showStep('coverage');
            
            // Check if we need additional Q&A based on coverage
            if (data.coverage_analysis && data.coverage_analysis.editable_recommendations && 
                data.coverage_analysis.editable_recommendations.length === 0) {
                // If no recommendations needed, skip to generation
                const buttonText = this.documentType === 'brd' ? 'Generate BRD' : 
                                 this.documentType === 'frd' ? 'Generate FRD' : 
                                 this.documentType === 'srd' ? 'Generate SRD' : 'Generate Enterprise Story';
                document.getElementById('generate-btn').textContent = buttonText;
            } else {
                // Set appropriate button text for generation with Q&A
                const buttonText = this.documentType === 'brd' ? 'Generate BRD from Analysis' : 
                                 this.documentType === 'frd' ? 'Generate FRD from Analysis' : 
                                 this.documentType === 'srd' ? 'Generate SRD from Analysis' : 'Generate Enterprise Story';
                document.getElementById('generate-btn').textContent = buttonText;
            }

        } catch (error) {
            this.showError(`Analysis failed: ${error.message}`);
        } finally {
            this.hideLoading();
        }
    }

    renderCoverageAnalysis(coverageData) {
        console.log('Rendering coverage data:', coverageData);
        
        // Check if coverageData exists and has proper structure
        if (!coverageData) {
            console.error('No coverage data received');
            return;
        }
        
        // Handle nested coverage_analysis structure
        if (coverageData.coverage_analysis) {
            coverageData = coverageData.coverage_analysis;
        }
        
        console.log('Coverage analysis rendered successfully');

        // Render present elements
        const presentList = document.getElementById('present-list');
        if (presentList) {
            presentList.innerHTML = '';
            
            console.log('Present elements:', coverageData.present_elements);
            
            if (coverageData.present_elements && coverageData.present_elements.length > 0) {
                coverageData.present_elements.forEach(element => {
                    const elementDiv = document.createElement('div');
                    elementDiv.className = 'element-item';
                    elementDiv.innerHTML = `
                        <h4>✅ ${element.element}</h4>
                        <p>${element.details || 'No details provided'}</p>
                    `;
                    presentList.appendChild(elementDiv);
                });
            } else {
                presentList.innerHTML = '<p>No elements fully covered yet.</p>';
            }
        }

        // Render missing elements
        const missingList = document.getElementById('missing-list');
        if (missingList) {
            missingList.innerHTML = '';
            
            console.log('Missing elements:', coverageData.missing_elements);
            
            if (coverageData.missing_elements && coverageData.missing_elements.length > 0) {
                coverageData.missing_elements.forEach(element => {
                    const elementDiv = document.createElement('div');
                    elementDiv.className = 'element-item';
                    elementDiv.innerHTML = `
                        <h4>❌ ${element.element}</h4>
                        <p>${element.details || 'No details provided'}</p>
                    `;
                    missingList.appendChild(elementDiv);
                });
            } else {
                missingList.innerHTML = '<p>All elements are covered! 🎉</p>';
            }
        }

        // Render editable recommendations - use missing elements if editable_recommendations is empty
        let recommendations = coverageData.editable_recommendations || [];
        
        // If no editable_recommendations, create them from missing_elements
        if (recommendations.length === 0 && coverageData.missing_elements) {
            recommendations = coverageData.missing_elements.map(element => ({
                element: element.element,
                question: `Please provide details for ${element.element}`,
                suggested_answer: element.suggested_content || `Provide ${element.element.toLowerCase()} requirements`,
                field_type: 'textarea'
            }));
        }
        
        this.renderRecommendations(recommendations);
        
        // Show generate button
        document.getElementById('generate-btn').style.display = 'inline-block';
    }

    renderRecommendations(recommendations) {
        const container = document.getElementById('recommendations-container');
        if (!container) return;
        
        container.innerHTML = '';

        if (!recommendations || recommendations.length === 0) {
            container.innerHTML = '<p>All enterprise elements are covered! Ready to generate story.</p>';
            return;
        }

        console.log('Rendering recommendations:', recommendations);

        recommendations.forEach((rec, index) => {
            const recDiv = document.createElement('div');
            recDiv.className = 'recommendation-item';
            
            const fieldId = `rec-${index}`;
            
            recDiv.innerHTML = `
                <h4>${rec.element}: ${rec.question || `Please provide ${rec.element} details`}</h4>
                <textarea id="${fieldId}" data-element="${rec.element}" 
                          placeholder="Enter your requirements...">${rec.suggested_answer || ''}</textarea>
            `;
            
            container.appendChild(recDiv);
        });
    }

    collectRecommendationAnswers() {
        const answers = {};
        const textareas = document.querySelectorAll('#recommendations-container textarea[data-element]');
        
        textareas.forEach(textarea => {
            const element = textarea.dataset.element;
            const value = textarea.value.trim();
            if (value) {
                answers[element] = value;
            }
        });

        return answers;
    }

    async generateDocument() {
        // Collect answers from recommendations
        const recAnswers = this.collectRecommendationAnswers();
        
        // Merge with any existing answers
        this.currentAnswers = { ...this.currentAnswers, ...recAnswers };
        
        const loadingMessage = this.documentType === 'brd' ? 
            'Generating comprehensive Business Requirements Document...' : 
            this.documentType === 'frd' ? 
            'Generating comprehensive Functional Requirements Document...' :
            this.documentType === 'srd' ? 
            'Generating comprehensive System Requirements Document...' :
            'Generating enterprise-ready user story...';
        
        this.showLoading(loadingMessage);

        try {
            // Choose endpoint based on document type
            const endpoint = this.documentType === 'brd' ? '/generate_brd' : 
                           this.documentType === 'frd' ? '/generate_frd' : 
                           this.documentType === 'srd' ? '/generate_srd' : '/generate';
            
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    requirement: this.currentRequirement,
                    answers: this.currentAnswers,
                    coverage_analysis: this.coverageData
                })
            });

            const data = await response.json();

            if (!response.ok) {
                const errorMessage = this.documentType === 'brd' ? 'BRD generation failed' : 'Story generation failed';
                throw new Error(data.error || errorMessage);
            }

            this.currentDocument = data;
            
            if (this.documentType === 'brd') {
                this.renderBRD(data);
            } else if (this.documentType === 'frd') {
                this.renderFRD(data);
            } else if (this.documentType === 'srd') {
                this.renderSRD(data);
            } else {
                this.renderStory(data);
            }
            
            this.updateUIForDocumentType();
            this.showStep('story');

        } catch (error) {
            const errorPrefix = this.documentType === 'brd' ? 'BRD generation failed' : 'Story generation failed';
            this.showError(`${errorPrefix}: ${error.message}`);
        } finally {
            this.hideLoading();
        }
    }

    renderStory(storyData) {
        const container = document.getElementById('story-container');
        container.innerHTML = '';

        // Helper function to render text sections with image support
        const renderTextSection = (title, content, sectionId) => {
            if (content) {
                const sectionDiv = document.createElement('div');
                sectionDiv.className = 'story-section';
                sectionDiv.innerHTML = `
                    <div class="section-header">
                        <h3>${title}</h3>
                        <button class="add-image-btn" onclick="app.addImageToSection('${sectionId}')" title="Add Image">
                            📷 Add Image
                        </button>
                    </div>
                    <p>${content}</p>
                    <div class="section-images" id="images-${sectionId}"></div>
                `;
                container.appendChild(sectionDiv);
            }
        };

        // Helper function to render array sections with image support
        const renderArraySection = (title, items, sectionId) => {
            if (items && items.length > 0) {
                const sectionDiv = document.createElement('div');
                sectionDiv.className = 'story-section';
                const itemsList = items.map(item => `<li>${item}</li>`).join('');
                sectionDiv.innerHTML = `
                    <div class="section-header">
                        <h3>${title}</h3>
                        <button class="add-image-btn" onclick="app.addImageToSection('${sectionId}')" title="Add Image">
                            📷 Add Image
                        </button>
                    </div>
                    <ul>${itemsList}</ul>
                    <div class="section-images" id="images-${sectionId}"></div>
                `;
                container.appendChild(sectionDiv);
            }
        };

        // Render all 10 enterprise elements with image support
        renderTextSection('🎯 Business Goal', storyData.business_goal, 'business-goal');
        renderTextSection('👤 Actor', storyData.actor, 'actor');
        renderTextSection('⚡ Trigger', storyData.trigger, 'trigger');
        renderArraySection('📋 Preconditions', storyData.preconditions, 'preconditions');
        renderArraySection('🔄 Functional Flow', storyData.functional_flow, 'functional-flow');
        renderArraySection('✅ Validations', storyData.validations, 'validations');
        renderArraySection('🎯 Acceptance Criteria', storyData.acceptance_criteria, 'acceptance-criteria');
        renderArraySection('🔒 Security', storyData.security, 'security');
        renderArraySection('🔗 Dependencies', storyData.dependencies, 'dependencies');
        renderArraySection('⚠️ Risks', storyData.risks, 'risks');
    }

    renderBRD(brdData) {
        const container = document.getElementById('story-container');
        container.innerHTML = '';

        // Helper function to render text sections with image support
        const renderTextSection = (title, content, sectionId) => {
            if (content) {
                const sectionDiv = document.createElement('div');
                sectionDiv.className = 'story-section';
                sectionDiv.innerHTML = `
                    <div class="section-header">
                        <h3>${title}</h3>
                        <button class="add-image-btn" onclick="app.addImageToSection('${sectionId}')" title="Add Image">
                            📷 Add Image
                        </button>
                    </div>
                    <p>${content}</p>
                    <div class="section-images" id="images-${sectionId}"></div>
                `;
                container.appendChild(sectionDiv);
            }
        };

        // Helper function to render array sections with image support
        const renderArraySection = (title, items, sectionId) => {
            if (items && items.length > 0) {
                const sectionDiv = document.createElement('div');
                sectionDiv.className = 'story-section';
                const itemsList = items.map(item => `<li>${item}</li>`).join('');
                sectionDiv.innerHTML = `
                    <div class="section-header">
                        <h3>${title}</h3>
                        <button class="add-image-btn" onclick="app.addImageToSection('${sectionId}')" title="Add Image">
                            📷 Add Image
                        </button>
                    </div>
                    <ul>${itemsList}</ul>
                    <div class="section-images" id="images-${sectionId}"></div>
                `;
                container.appendChild(sectionDiv);
            }
        };

        // Helper function to render object sections
        const renderObjectSection = (title, obj, sectionId) => {
            if (obj && typeof obj === 'object') {
                const sectionDiv = document.createElement('div');
                sectionDiv.className = 'story-section';
                let content = `
                    <div class="section-header">
                        <h3>${title}</h3>
                        <button class="add-image-btn" onclick="app.addImageToSection('${sectionId}')" title="Add Image">
                            📷 Add Image
                        </button>
                    </div>
                `;
                
                Object.entries(obj).forEach(([key, value]) => {
                    if (Array.isArray(value)) {
                        content += `<h4>${key.replace('_', ' ').toUpperCase()}:</h4><ul>`;
                        value.forEach(item => {
                            content += `<li>${item}</li>`;
                        });
                        content += `</ul>`;
                    } else {
                        content += `<h4>${key.replace('_', ' ').toUpperCase()}:</h4><p>${value}</p>`;
                    }
                });
                
                content += `<div class="section-images" id="images-${sectionId}"></div>`;
                sectionDiv.innerHTML = content;
                container.appendChild(sectionDiv);
            }
        };

        // Helper function to render table sections
        const renderTableSection = (title, items, columns, sectionId) => {
            if (items && items.length > 0) {
                const sectionDiv = document.createElement('div');
                sectionDiv.className = 'story-section';
                
                let tableHTML = `
                    <div class="section-header">
                        <h3>${title}</h3>
                        <button class="add-image-btn" onclick="app.addImageToSection('${sectionId}')" title="Add Image">
                            📷 Add Image
                        </button>
                    </div>
                    <table style="width: 100%; border-collapse: collapse; margin-top: 10px;">
                `;
                
                // Header row
                tableHTML += '<tr>';
                columns.forEach(col => {
                    tableHTML += `<th style="border: 1px solid #ddd; padding: 8px; background-color: #f2f2f2; text-align: left;">${col}</th>`;
                });
                tableHTML += '</tr>';
                
                // Data rows
                items.forEach(item => {
                    tableHTML += '<tr>';
                    columns.forEach(col => {
                        const key = col.toLowerCase().replace(' ', '_');
                        tableHTML += `<td style="border: 1px solid #ddd; padding: 8px;">${item[key] || ''}</td>`;
                    });
                    tableHTML += '</tr>';
                });
                
                tableHTML += `</table><div class="section-images" id="images-${sectionId}"></div>`;
                sectionDiv.innerHTML = tableHTML;
                container.appendChild(sectionDiv);
            }
        };

        // Render all 15 BRD sections with image support
        renderTextSection('📋 Project Name', brdData.project_name, 'project-name');
        
        if (brdData.executive_summary) {
            renderObjectSection('📊 Executive Summary', brdData.executive_summary, 'executive-summary');
        }
        
        if (brdData.business_objectives) {
            renderTableSection('🎯 Business Objectives', brdData.business_objectives, ['Objective', 'KPI'], 'business-objectives');
        }
        
        if (brdData.scope) {
            renderObjectSection('🔍 Project Scope', brdData.scope, 'scope');
        }
        
        if (brdData.stakeholders) {
            renderTableSection('👥 Stakeholder List', brdData.stakeholders, ['Name', 'Role', 'Department', 'Responsibilities'], 'stakeholders');
        }
        
        if (brdData.current_state) {
            renderObjectSection('📈 Current State Analysis', brdData.current_state, 'current-state');
        }
        
        if (brdData.future_state) {
            renderObjectSection('🚀 Future State Vision', brdData.future_state, 'future-state');
        }
        
        if (brdData.business_requirements) {
            renderTableSection('📋 Business Requirements', brdData.business_requirements, ['BR ID', 'Title', 'Description', 'Priority', 'Source', 'Acceptance Criteria'], 'business-requirements');
        }
        
        if (brdData.business_rules) {
            renderTableSection('📏 Business Rules', brdData.business_rules, ['Rule ID', 'Description'], 'business-rules');
        }
        
        renderArraySection('💭 Assumptions', brdData.assumptions, 'assumptions');
        renderArraySection('🔗 Dependencies', brdData.dependencies, 'dependencies');
        
        if (brdData.risks) {
            renderTableSection('⚠️ Risk Assessment', brdData.risks, ['Risk ID', 'Description', 'Impact', 'Likelihood', 'Mitigation'], 'risks');
        }
        
        if (brdData.success_metrics) {
            renderTableSection('📊 Success Metrics', brdData.success_metrics, ['Metric Name', 'Measurement Method', 'Target Value', 'Monitoring Frequency'], 'success-metrics');
        }
        
        if (brdData.glossary) {
            renderTableSection('📖 Glossary', brdData.glossary, ['Term', 'Definition'], 'glossary');
        }
        
        if (brdData.approval_workflow) {
            renderTableSection('✅ Approval Workflow', brdData.approval_workflow, ['Step', 'Approver Role', 'Approver Name', 'Approval Criteria'], 'approval-workflow');
        }
        
        renderArraySection('📎 Supporting Documents', brdData.supporting_documents, 'supporting-documents');
    }

    renderFRD(frdData) {
        const container = document.getElementById('story-container');
        container.innerHTML = '';

        // Helper function to render text sections with image support
        const renderTextSection = (title, content, sectionId) => {
            if (content) {
                const sectionDiv = document.createElement('div');
                sectionDiv.className = 'story-section';
                sectionDiv.innerHTML = `
                    <div class="section-header">
                        <h3>${title}</h3>
                        <button class="add-image-btn" onclick="app.addImageToSection('${sectionId}')" title="Add Image">
                            📷 Add Image
                        </button>
                    </div>
                    <p>${content}</p>
                    <div class="section-images" id="images-${sectionId}"></div>
                `;
                container.appendChild(sectionDiv);
            }
        };

        // Helper function to render array sections with image support
        const renderArraySection = (title, items, sectionId) => {
            if (items && items.length > 0) {
                const sectionDiv = document.createElement('div');
                sectionDiv.className = 'story-section';
                const itemsList = items.map(item => `<li>${item}</li>`).join('');
                sectionDiv.innerHTML = `
                    <div class="section-header">
                        <h3>${title}</h3>
                        <button class="add-image-btn" onclick="app.addImageToSection('${sectionId}')" title="Add Image">
                            📷 Add Image
                        </button>
                    </div>
                    <ul>${itemsList}</ul>
                    <div class="section-images" id="images-${sectionId}"></div>
                `;
                container.appendChild(sectionDiv);
            }
        };

        // Helper function to render object sections
        const renderObjectSection = (title, obj, sectionId) => {
            if (obj && typeof obj === 'object') {
                const sectionDiv = document.createElement('div');
                sectionDiv.className = 'story-section';
                let content = `
                    <div class="section-header">
                        <h3>${title}</h3>
                        <button class="add-image-btn" onclick="app.addImageToSection('${sectionId}')" title="Add Image">
                            📷 Add Image
                        </button>
                    </div>
                `;
                
                Object.entries(obj).forEach(([key, value]) => {
                    if (Array.isArray(value)) {
                        content += `<h4>${key.replace('_', ' ').toUpperCase()}:</h4><ul>`;
                        value.forEach(item => {
                            content += `<li>${item}</li>`;
                        });
                        content += `</ul>`;
                    } else {
                        content += `<h4>${key.replace('_', ' ').toUpperCase()}:</h4><p>${value}</p>`;
                    }
                });
                
                content += `<div class="section-images" id="images-${sectionId}"></div>`;
                sectionDiv.innerHTML = content;
                container.appendChild(sectionDiv);
            }
        };

        // Helper function to render table sections
        const renderTableSection = (title, items, columns, sectionId) => {
            if (items && items.length > 0) {
                const sectionDiv = document.createElement('div');
                sectionDiv.className = 'story-section';
                
                let tableHTML = `
                    <div class="section-header">
                        <h3>${title}</h3>
                        <button class="add-image-btn" onclick="app.addImageToSection('${sectionId}')" title="Add Image">
                            📷 Add Image
                        </button>
                    </div>
                    <table style="width: 100%; border-collapse: collapse; margin-top: 10px;">
                `;
                
                // Header row
                tableHTML += '<tr>';
                columns.forEach(col => {
                    tableHTML += `<th style="border: 1px solid #ddd; padding: 8px; background-color: #f2f2f2; text-align: left;">${col}</th>`;
                });
                tableHTML += '</tr>';
                
                // Data rows
                items.forEach(item => {
                    tableHTML += '<tr>';
                    columns.forEach(col => {
                        const key = col.toLowerCase().replace(' ', '_');
                        tableHTML += `<td style="border: 1px solid #ddd; padding: 8px;">${item[key] || ''}</td>`;
                    });
                    tableHTML += '</tr>';
                });
                
                tableHTML += `</table><div class="section-images" id="images-${sectionId}"></div>`;
                sectionDiv.innerHTML = tableHTML;
                container.appendChild(sectionDiv);
            }
        };

        // Render all 14 FRD sections with image support
        if (frdData.system_overview) {
            renderObjectSection('🏗️ System Overview', frdData.system_overview, 'system-overview');
        }
        
        if (frdData.functional_requirements) {
            renderTableSection('⚙️ Functional Requirements', frdData.functional_requirements, ['Req ID', 'Title', 'Description', 'Priority', 'Acceptance Criteria'], 'functional-requirements');
        }
        
        if (frdData.data_requirements) {
            renderObjectSection('💾 Data Requirements', frdData.data_requirements, 'data-requirements');
        }
        
        if (frdData.interface_requirements) {
            renderObjectSection('🖥️ Interface Requirements', frdData.interface_requirements, 'interface-requirements');
        }
        
        if (frdData.integration_requirements) {
            renderTableSection('🔗 Integration Requirements', frdData.integration_requirements, ['System', 'Method', 'Data Format', 'Frequency'], 'integration-requirements');
        }
        
        if (frdData.performance_requirements) {
            renderObjectSection('⚡ Performance Requirements', frdData.performance_requirements, 'performance-requirements');
        }
        
        renderArraySection('🔒 Security Requirements', frdData.security_requirements, 'security-requirements');
        
        if (frdData.validation_rules) {
            renderTableSection('✅ Validation Rules', frdData.validation_rules, ['Field', 'Rule', 'Error Message'], 'validation-rules');
        }
        
        if (frdData.error_handling) {
            renderTableSection('❌ Error Handling', frdData.error_handling, ['Error Type', 'Handling Strategy', 'User Message', 'Logging'], 'error-handling');
        }
        
        if (frdData.reporting_requirements) {
            renderTableSection('📊 Reporting Requirements', frdData.reporting_requirements, ['Report Name', 'Description', 'Frequency', 'Format'], 'reporting-requirements');
        }
        
        if (frdData.testing_requirements) {
            renderObjectSection('🧪 Testing Requirements', frdData.testing_requirements, 'testing-requirements');
        }
        
        if (frdData.deployment_requirements) {
            renderObjectSection('🚀 Deployment Requirements', frdData.deployment_requirements, 'deployment-requirements');
        }
        
        if (frdData.maintenance_requirements) {
            renderObjectSection('🔧 Maintenance Requirements', frdData.maintenance_requirements, 'maintenance-requirements');
        }
        
        if (frdData.technical_specifications) {
            renderTableSection('⚙️ Technical Specifications', frdData.technical_specifications, ['Component', 'Specification'], 'technical-specifications');
        }
    }

    renderSRD(srdData) {
        const container = document.getElementById('story-container');
        container.innerHTML = '';

        // Helper function to render text sections with image support
        const renderTextSection = (title, content, sectionId) => {
            if (content) {
                const sectionDiv = document.createElement('div');
                sectionDiv.className = 'story-section';
                sectionDiv.innerHTML = `
                    <div class="section-header">
                        <h3>${title}</h3>
                        <button class="add-image-btn" onclick="app.addImageToSection('${sectionId}')" title="Add Image">
                            📷 Add Image
                        </button>
                    </div>
                    <p>${content}</p>
                    <div class="section-images" id="images-${sectionId}"></div>
                `;
                container.appendChild(sectionDiv);
            }
        };

        // Helper function to render array sections with image support
        const renderArraySection = (title, items, sectionId) => {
            if (items && items.length > 0) {
                const sectionDiv = document.createElement('div');
                sectionDiv.className = 'story-section';
                const itemsList = items.map(item => `<li>${item}</li>`).join('');
                sectionDiv.innerHTML = `
                    <div class="section-header">
                        <h3>${title}</h3>
                        <button class="add-image-btn" onclick="app.addImageToSection('${sectionId}')" title="Add Image">
                            📷 Add Image
                        </button>
                    </div>
                    <ul>${itemsList}</ul>
                    <div class="section-images" id="images-${sectionId}"></div>
                `;
                container.appendChild(sectionDiv);
            }
        };

        // Helper function to render object sections
        const renderObjectSection = (title, obj, sectionId) => {
            if (obj && typeof obj === 'object') {
                const sectionDiv = document.createElement('div');
                sectionDiv.className = 'story-section';
                let content = `
                    <div class="section-header">
                        <h3>${title}</h3>
                        <button class="add-image-btn" onclick="app.addImageToSection('${sectionId}')" title="Add Image">
                            📷 Add Image
                        </button>
                    </div>
                `;
                
                Object.entries(obj).forEach(([key, value]) => {
                    if (Array.isArray(value)) {
                        content += `<h4>${key.replace('_', ' ').toUpperCase()}:</h4><ul>`;
                        value.forEach(item => {
                            content += `<li>${item}</li>`;
                        });
                        content += `</ul>`;
                    } else {
                        content += `<h4>${key.replace('_', ' ').toUpperCase()}:</h4><p>${value}</p>`;
                    }
                });
                
                content += `<div class="section-images" id="images-${sectionId}"></div>`;
                sectionDiv.innerHTML = content;
                container.appendChild(sectionDiv);
            }
        };

        // Helper function to render table sections
        const renderTableSection = (title, items, columns, sectionId) => {
            if (items && items.length > 0) {
                const sectionDiv = document.createElement('div');
                sectionDiv.className = 'story-section';
                
                let tableHTML = `
                    <div class="section-header">
                        <h3>${title}</h3>
                        <button class="add-image-btn" onclick="app.addImageToSection('${sectionId}')" title="Add Image">
                            📷 Add Image
                        </button>
                    </div>
                    <table style="width: 100%; border-collapse: collapse; margin-top: 10px;">
                `;
                
                // Header row
                tableHTML += '<tr>';
                columns.forEach(col => {
                    tableHTML += `<th style="border: 1px solid #ddd; padding: 8px; background-color: #f2f2f2; text-align: left;">${col}</th>`;
                });
                tableHTML += '</tr>';
                
                // Data rows
                items.forEach(item => {
                    tableHTML += '<tr>';
                    columns.forEach(col => {
                        const key = col.toLowerCase().replace(' ', '_');
                        tableHTML += `<td style="border: 1px solid #ddd; padding: 8px;">${item[key] || ''}</td>`;
                    });
                    tableHTML += '</tr>';
                });
                
                tableHTML += `</table><div class="section-images" id="images-${sectionId}"></div>`;
                sectionDiv.innerHTML = tableHTML;
                container.appendChild(sectionDiv);
            }
        };

        // Render all 12 SRD sections with image support
        if (srdData.system_architecture) {
            renderObjectSection('🏗️ System Architecture', srdData.system_architecture, 'system-architecture');
        }
        
        if (srdData.hardware_requirements) {
            renderObjectSection('💻 Hardware Requirements', srdData.hardware_requirements, 'hardware-requirements');
        }
        
        if (srdData.software_requirements) {
            renderObjectSection('💿 Software Requirements', srdData.software_requirements, 'software-requirements');
        }
        
        if (srdData.network_requirements) {
            renderObjectSection('🌐 Network Requirements', srdData.network_requirements, 'network-requirements');
        }
        
        if (srdData.database_requirements) {
            renderObjectSection('💾 Database Requirements', srdData.database_requirements, 'database-requirements');
        }
        
        if (srdData.system_interfaces) {
            renderTableSection('🔗 System Interfaces', srdData.system_interfaces, ['Interface', 'Type', 'Protocol', 'Data Format'], 'system-interfaces');
        }
        
        if (srdData.performance_specifications) {
            renderObjectSection('⚡ Performance Specifications', srdData.performance_specifications, 'performance-specifications');
        }
        
        if (srdData.security_architecture) {
            renderObjectSection('🔒 Security Architecture', srdData.security_architecture, 'security-architecture');
        }
        
        if (srdData.backup_recovery) {
            renderObjectSection('💾 Backup & Recovery', srdData.backup_recovery, 'backup-recovery');
        }
        
        if (srdData.monitoring_logging) {
            renderObjectSection('📊 Monitoring & Logging', srdData.monitoring_logging, 'monitoring-logging');
        }
        
        if (srdData.scalability_requirements) {
            renderObjectSection('📈 Scalability Requirements', srdData.scalability_requirements, 'scalability-requirements');
        }
        
        if (srdData.compliance_standards) {
            renderTableSection('✅ Compliance Standards', srdData.compliance_standards, ['Standard', 'Description'], 'compliance-standards');
        }
    }

    async exportDocument(format) {
        if (!this.currentDocument) {
            this.showError('No document to export');
            return;
        }

        this.showLoading(`Exporting to ${format.toUpperCase()}...`);

        try {
            // Choose endpoint based on document type
            const endpoint = this.documentType === 'brd' ? `/export_brd/${format}` : 
                           this.documentType === 'frd' ? `/export_frd/${format}` : 
                           this.documentType === 'srd' ? `/export_srd/${format}` : `/export/${format}`;
            const dataKey = this.documentType === 'brd' ? 'brd_data' : 
                          this.documentType === 'frd' ? 'frd_data' : 
                          this.documentType === 'srd' ? 'srd_data' : 'story_data';
            
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    [dataKey]: this.currentDocument,
                    coverage_data: this.coverageData,
                    section_images: this.sectionImages
                })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Export failed');
            }

            // Download the file
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            
            const fileNames = {
                'user-story': `enterprise_user_story.${format === 'word' ? 'docx' : format}`,
                'brd': `business_requirements_document.${format === 'word' ? 'docx' : format}`,
                'frd': `functional_requirements_document.${format === 'word' ? 'docx' : format}`,
                'srd': `system_requirements_document.${format === 'word' ? 'docx' : format}`
            };
            
            a.download = fileNames[this.documentType] || `document.${format === 'word' ? 'docx' : format}`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);

        } catch (error) {
            this.showError(`Export failed: ${error.message}`);
        } finally {
            this.hideLoading();
        }
    }

    startOver() {
        this.currentRequirement = '';
        this.currentAnswers = {};
        this.currentDocument = null;
        this.coverageData = null;
        this.sectionImages = {};
        
        document.getElementById('requirement-input').value = '';
        document.getElementById('coverage-container').innerHTML = '';
        document.getElementById('questions-container').innerHTML = '';
        document.getElementById('story-container').innerHTML = '';
        document.getElementById('generate-btn').style.display = 'none';
        document.getElementById('generate-from-qa').style.display = 'none';
        
        // Reset tiles to default selection
        const tiles = document.querySelectorAll('.document-tile');
        tiles.forEach(tile => tile.classList.remove('selected'));
        
        const defaultTile = document.querySelector('.document-tile[data-type="user-story"]');
        if (defaultTile) {
            defaultTile.classList.add('selected');
        }
        
        this.documentType = 'user-story';
        document.getElementById('selected-document-type').value = 'user-story';
        this.updateAnalyzeButton('user-story');
        this.updateUIForDocumentType();
        
        this.showStep('requirement');
    }

    // Section image management methods
    addImageToSection(sectionId) {
        const input = document.createElement('input');
        input.type = 'file';
        input.accept = 'image/*';
        input.onchange = (e) => {
            const file = e.target.files[0];
            if (file) {
                this.processImageForSection(sectionId, file);
            }
        };
        input.click();
    }

    async processImageForSection(sectionId, file) {
        try {
            const base64 = await this.fileToBase64(file);
            
            if (!this.sectionImages[sectionId]) {
                this.sectionImages[sectionId] = [];
            }
            
            const imageData = {
                name: file.name,
                data: base64,
                caption: ''
            };
            
            this.sectionImages[sectionId].push(imageData);
            this.renderSectionImages(sectionId);
        } catch (error) {
            this.showError(`Failed to process image: ${error.message}`);
        }
    }

    renderSectionImages(sectionId) {
        const container = document.getElementById(`images-${sectionId}`);
        if (!container || !this.sectionImages[sectionId]) return;

        container.innerHTML = '';
        
        this.sectionImages[sectionId].forEach((image, index) => {
            const imageDiv = document.createElement('div');
            imageDiv.className = 'section-image';
            imageDiv.innerHTML = `
                <img src="${image.data}" alt="${image.name}" style="max-width: 300px; max-height: 200px;">
                <input type="text" placeholder="Add caption..." value="${image.caption}" 
                       onchange="app.updateImageCaption('${sectionId}', ${index}, this.value)">
                <button onclick="app.removeImageFromSection('${sectionId}', ${index})" title="Remove">×</button>
            `;
            container.appendChild(imageDiv);
        });
    }

    updateImageCaption(sectionId, imageIndex, caption) {
        if (this.sectionImages[sectionId] && this.sectionImages[sectionId][imageIndex]) {
            this.sectionImages[sectionId][imageIndex].caption = caption;
        }
    }

    removeImageFromSection(sectionId, imageIndex) {
        if (this.sectionImages[sectionId]) {
            this.sectionImages[sectionId].splice(imageIndex, 1);
            this.renderSectionImages(sectionId);
        }
    }

    fileToBase64(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.readAsDataURL(file);
            reader.onload = () => resolve(reader.result);
            reader.onerror = error => reject(error);
        });
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.app = new DocumentGeneratorApp();
});